package org.interdependency.ahbg

import org.json.JSONObject
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

/**
 * Minimal HTTP client for the canonical runtime bridge.
 *
 * Speaks the same observe/plan/act JSON contract as the in-process harness.
 * The Android layer only transports JSON; the canonical runtime owns all game
 * state and geometry.
 */
class HarnessClient(private val baseUrl: String) {

    fun get(path: String): String {
        val connection = (URL(baseUrl + path).openConnection() as HttpURLConnection).apply {
            requestMethod = "GET"
            connectTimeout = 5000
            readTimeout = 5000
        }
        return connection.inputStream.bufferedReader().use(BufferedReader::readText)
    }

    fun post(path: String, body: String): String {
        val connection = (URL(baseUrl + path).openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            connectTimeout = 5000
            readTimeout = 5000
            doOutput = true
            setRequestProperty("Content-Type", "application/json; charset=utf-8")
        }
        OutputStreamWriter(connection.outputStream).use { it.write(body) }
        return try {
            connection.inputStream.bufferedReader().use(BufferedReader::readText)
        } catch (error: java.io.IOException) {
            connection.errorStream?.bufferedReader()?.use(BufferedReader::readText) ?: "{\"error\":\"${error.message}\"}"
        }
    }

    companion object {
        fun jsonString(value: String): String = JSONObject.quote(value)
    }
}
