package org.interdependency.ahbg

import android.annotation.SuppressLint
import android.app.Activity
import android.net.Uri
import android.os.Bundle
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient

/** Same-origin phone client. The server owns player identity, orders and the turn journal. */
class MainActivity : Activity() {
    private lateinit var board: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val origin = Uri.parse(BuildConfig.RUNTIME_URL)
        require(origin.scheme == "https" || BuildConfig.DEBUG && origin.host in setOf("10.0.2.2", "localhost"))
        board = WebView(this).apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            settings.mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_NEVER_ALLOW
            CookieManager.getInstance().setAcceptThirdPartyCookies(this, false)
            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean =
                    request.url.scheme != origin.scheme || request.url.host != origin.host || request.url.port != origin.port
            }
            loadUrl("${BuildConfig.RUNTIME_URL.trimEnd('/')}/board.html")
        }
        setContentView(board)
    }

    override fun onPause() {
        CookieManager.getInstance().flush()
        super.onPause()
    }

    override fun onDestroy() {
        board.destroy()
        super.onDestroy()
    }
}
