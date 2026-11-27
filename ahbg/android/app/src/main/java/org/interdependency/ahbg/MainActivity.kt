package org.interdependency.ahbg

import android.annotation.SuppressLint
import android.app.Activity
import android.net.ConnectivityManager
import android.net.Network
import android.net.Uri
import android.os.Bundle
import android.webkit.CookieManager
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient

/** Same-origin phone client. The server owns player identity, orders and the turn journal. */
class MainActivity : Activity() {
    private lateinit var board: WebView
    private lateinit var recovery: LinearLayout
    private lateinit var network: ConnectivityManager
    private var offline = false
    private val connectivity = object : ConnectivityManager.NetworkCallback() {
        override fun onAvailable(network: Network) {
            runOnUiThread { if (offline && !isDestroyed) reloadBoard() }
        }
    }

    private fun reloadBoard() {
        offline = false
        recovery.visibility = View.GONE
        board.visibility = View.VISIBLE
        board.loadUrl("${BuildConfig.RUNTIME_URL.trimEnd('/')}/board.html")
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val origin = Uri.parse(BuildConfig.RUNTIME_URL)
        require(origin.scheme == "https" || BuildConfig.DEBUG && origin.host in setOf("10.0.2.2", "localhost"))
        val premium = lazy { PremiumStore.create(this, BuildConfig.REVENUECAT_API_KEY) }
        recovery = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            addView(TextView(context).apply { text = "Connection interrupted. Your plane is saved on the VM." })
            addView(Button(context).apply { text = "Reconnect"; setOnClickListener { reloadBoard() } })
            visibility = View.GONE
        }
        board = WebView(this).apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_NEVER_ALLOW
            CookieManager.getInstance().setAcceptThirdPartyCookies(this, false)
            webViewClient = object : WebViewClient() {
                override fun onReceivedError(view: WebView, request: WebResourceRequest, error: WebResourceError) {
                    if (request.isForMainFrame) {
                        offline = true
                        view.visibility = View.GONE
                        recovery.visibility = View.VISIBLE
                    }
                }

                override fun onPageFinished(view: WebView, url: String) {
                    val page = Uri.parse(url)
                    if (page.scheme != origin.scheme || page.authority != origin.authority) return
                    // The legacy board reads this entitlement. No web content can call native methods.
                    view.evaluateJavascript("Boolean(document.getElementById('premium-status'))") { present ->
                        if (present == "true" && !isDestroyed) {
                            val label = if (premium.value.isBenchmarkLabUnlocked()) "unlocked" else "locked (basic play free)"
                            view.evaluateJavascript("document.getElementById('premium-status')?.replaceChildren('Benchmark Lab: $label')", null)
                        }
                    }
                }

                override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean =
                    request.url.scheme != origin.scheme || request.url.host != origin.host || request.url.port != origin.port
            }
        }
        setContentView(LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            addView(recovery)
            addView(board, LinearLayout.LayoutParams(-1, -1))
        })
        network = getSystemService(ConnectivityManager::class.java)
        network.registerDefaultNetworkCallback(connectivity)
        reloadBoard()
    }

    override fun onPause() {
        CookieManager.getInstance().flush()
        super.onPause()
    }

    override fun onDestroy() {
        network.unregisterNetworkCallback(connectivity)
        board.destroy()
        super.onDestroy()
    }
}
