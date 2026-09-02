package org.interdependency.ahbg

import android.annotation.SuppressLint
import android.app.Activity
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import org.json.JSONObject

/**
 * Thinnest Android-first shell around the canonical AHBG runtime.
 *
 * This activity hosts the canonical presentation board in a WebView and
 * exposes one small JS bridge (`window.ahbg`) that forwards observe/plan/act
 * calls to the runtime HTTP bridge plus the Android-owned RevenueCat purchase
 * and restore operations. The mobile layer presents and controls AHBG; it is
 * not a second game engine and never reimplements UCNS geometry.
 */
class MainActivity : Activity() {

    private lateinit var webView: WebView
    private lateinit var harnessClient: HarnessClient
    private lateinit var premiumStore: PremiumStore

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        harnessClient = HarnessClient(BuildConfig.RUNTIME_URL)
        premiumStore = PremiumStore.create(this, BuildConfig.REVENUECAT_API_KEY)

        webView = WebView(this).apply {
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            webViewClient = WebViewClient()
            addJavascriptInterface(Bridge(), "ahbg")
            loadUrl("${BuildConfig.RUNTIME_URL}/board.html")
        }
        setContentView(webView)
    }

    private fun toast(message: String) {
        runOnUiThread { Toast.makeText(this, message, Toast.LENGTH_SHORT).show() }
    }

    private fun returnPremiumResult(callbackId: String, result: PremiumActionResult) {
        val payload = JSONObject()
            .put("ok", result.ok)
            .put("unlocked", result.unlocked)
            .put("message", result.message)
            .toString()
        runOnUiThread {
            webView.evaluateJavascript(
                "window.ahbgPremiumResult(${JSONObject.quote(callbackId)}, ${JSONObject.quote(payload)});",
                null,
            )
        }
    }

    inner class Bridge {
        @JavascriptInterface
        fun startSession(seed: Int, turns: Int, callbackId: String) {
            Thread {
                val body = "{\"seed\":$seed,\"turns\":$turns}"
                val result = harnessClient.post("/session", body)
                runOnUiThread { webView.evaluateJavascript("window.ahbgCallback('$callbackId', ${json(result)});", null) }
            }.start()
        }

        @JavascriptInterface
        fun submitPlan(planJson: String, callbackId: String) {
            Thread {
                val sessionId = extractSessionId(planJson)
                val result = if (sessionId == null) {
                    "{\"error\":\"plan json must carry session_id\"}"
                } else {
                    harnessClient.post("/session/$sessionId/plan", "{\"plan\":$planJson}")
                }
                runOnUiThread { webView.evaluateJavascript("window.ahbgCallback('$callbackId', ${json(result)});", null) }
            }.start()
        }

        @JavascriptInterface
        fun getState(sessionId: String, callbackId: String) {
            Thread {
                val result = harnessClient.get("/session/$sessionId/state")
                runOnUiThread { webView.evaluateJavascript("window.ahbgCallback('$callbackId', ${json(result)});", null) }
            }.start()
        }

        @JavascriptInterface
        fun isBenchmarkLabUnlocked(): Boolean = premiumStore.isBenchmarkLabUnlocked()

        @JavascriptInterface
        fun purchaseBenchmarkLab(callbackId: String) {
            runOnUiThread {
                premiumStore.purchaseBenchmarkLab(this@MainActivity) { result ->
                    returnPremiumResult(callbackId, result)
                }
            }
        }

        @JavascriptInterface
        fun restoreBenchmarkLab(callbackId: String) {
            premiumStore.restoreBenchmarkLab { result ->
                returnPremiumResult(callbackId, result)
            }
        }

        private fun extractSessionId(planJson: String): String? {
            return Regex("\"session_id\"\\s*:\\s*\"([^\"]+)\"").find(planJson)?.groupValues?.get(1)
        }

        private fun json(value: String): String = JSONObject.quote(value)
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}
