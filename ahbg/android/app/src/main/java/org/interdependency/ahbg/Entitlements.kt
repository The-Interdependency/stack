package org.interdependency.ahbg

import android.app.Activity
import android.content.Context
import com.revenuecat.purchases.CustomerInfo
import com.revenuecat.purchases.Offerings
import com.revenuecat.purchases.PurchaseParams
import com.revenuecat.purchases.Purchases
import com.revenuecat.purchases.PurchasesConfiguration
import com.revenuecat.purchases.PurchasesError
import com.revenuecat.purchases.interfaces.PurchaseCallback
import com.revenuecat.purchases.interfaces.ReceiveCustomerInfoCallback
import com.revenuecat.purchases.interfaces.ReceiveOfferingsCallback
import com.revenuecat.purchases.models.StoreTransaction

/**
 * One clean entitlement: `benchmark_lab`.
 *
 * Basic gameplay and external harness connectivity are always free. Benchmark
 * Lab (advanced scenarios, saved/replayed run comparison, adversarial packs)
 * unlocks only when RevenueCat reports the `benchmark_lab` entitlement as
 * active for the current app user.
 *
 * RevenueCat 10.x core supports Google Play billing by default through the
 * ordinary `PurchasesConfiguration`; no store module is required.
 *
 * Usage: build the Play release with the app-specific RevenueCat public key
 * (`-PrevenueCatApiKey=goog_...`). The presentation bridge calls
 * `purchaseBenchmarkLab` and `restoreBenchmarkLab`; both return the resulting
 * entitlement state to the human-visible UI. Missing/invalid keys fail closed
 * to the free tier rather than entering a broken billing flow.
 */
data class PremiumActionResult(
    val ok: Boolean,
    val unlocked: Boolean,
    val message: String,
)

interface PremiumStore {
    fun isBenchmarkLabUnlocked(): Boolean
    fun purchaseBenchmarkLab(activity: Activity, callback: (PremiumActionResult) -> Unit)
    fun restoreBenchmarkLab(callback: (PremiumActionResult) -> Unit)

    companion object {
        const val ENTITLEMENT = "benchmark_lab"
        const val PRODUCT_ID = "ahbg_benchmark_lab"

        fun create(context: Context, revenueCatApiKey: String): PremiumStore {
            if (revenueCatApiKey.isBlank() || revenueCatApiKey.startsWith("REVENUECAT_KEY_NOT_PROVISIONED")) {
                return NoopPremiumStore("RevenueCat Google Play key is not provisioned")
            }
            if (!revenueCatApiKey.startsWith("goog_")) {
                return NoopPremiumStore("RevenueCat Google Play public SDK key must start with goog_")
            }
            return RevenueCatPremiumStore(context, revenueCatApiKey)
        }
    }
}

class NoopPremiumStore(
    private val reason: String = "RevenueCat is not provisioned",
) : PremiumStore {
    override fun isBenchmarkLabUnlocked(): Boolean = false

    override fun purchaseBenchmarkLab(activity: Activity, callback: (PremiumActionResult) -> Unit) {
        callback(PremiumActionResult(ok = false, unlocked = false, message = reason))
    }

    override fun restoreBenchmarkLab(callback: (PremiumActionResult) -> Unit) {
        callback(PremiumActionResult(ok = false, unlocked = false, message = reason))
    }
}

class RevenueCatPremiumStore(
    context: Context,
    apiKey: String,
) : PremiumStore {

    @Volatile
    private var benchmarkLabUnlocked: Boolean = false

    init {
        Purchases.configure(
            PurchasesConfiguration.Builder(context.applicationContext, apiKey).build()
        )
        refreshCustomerInfo()
    }

    private fun applyCustomerInfo(customerInfo: CustomerInfo): Boolean {
        benchmarkLabUnlocked =
            customerInfo.entitlements.active[PremiumStore.ENTITLEMENT]?.isActive == true
        return benchmarkLabUnlocked
    }

    private fun refreshCustomerInfo() {
        Purchases.sharedInstance.getCustomerInfo(object : ReceiveCustomerInfoCallback {
            override fun onReceived(customerInfo: CustomerInfo) {
                applyCustomerInfo(customerInfo)
            }

            override fun onError(error: PurchasesError) {
                benchmarkLabUnlocked = false
            }
        })
    }

    override fun isBenchmarkLabUnlocked(): Boolean = benchmarkLabUnlocked

    override fun purchaseBenchmarkLab(activity: Activity, callback: (PremiumActionResult) -> Unit) {
        Purchases.sharedInstance.getOfferings(object : ReceiveOfferingsCallback {
            override fun onReceived(offerings: Offerings) {
                val packageToPurchase = offerings.current?.availablePackages?.firstOrNull {
                    it.product.id == PremiumStore.PRODUCT_ID
                }
                if (packageToPurchase == null) {
                    callback(
                        PremiumActionResult(
                            ok = false,
                            unlocked = benchmarkLabUnlocked,
                            message = "Current RevenueCat offering does not contain ${PremiumStore.PRODUCT_ID}",
                        )
                    )
                    return
                }

                val params = PurchaseParams.Builder(activity, packageToPurchase).build()
                Purchases.sharedInstance.purchase(params, object : PurchaseCallback {
                    override fun onCompleted(storeTransaction: StoreTransaction, customerInfo: CustomerInfo) {
                        val unlocked = applyCustomerInfo(customerInfo)
                        callback(
                            PremiumActionResult(
                                ok = unlocked,
                                unlocked = unlocked,
                                message = if (unlocked) {
                                    "Benchmark Lab purchase active"
                                } else {
                                    "Purchase completed but benchmark_lab entitlement is not active"
                                },
                            )
                        )
                    }

                    override fun onError(error: PurchasesError, userCancelled: Boolean) {
                        callback(
                            PremiumActionResult(
                                ok = false,
                                unlocked = benchmarkLabUnlocked,
                                message = if (userCancelled) "Purchase cancelled" else "Purchase failed: ${error.message}",
                            )
                        )
                    }
                })
            }

            override fun onError(error: PurchasesError) {
                callback(
                    PremiumActionResult(
                        ok = false,
                        unlocked = benchmarkLabUnlocked,
                        message = "Could not load Benchmark Lab offering: ${error.message}",
                    )
                )
            }
        })
    }

    override fun restoreBenchmarkLab(callback: (PremiumActionResult) -> Unit) {
        Purchases.sharedInstance.restorePurchases(object : ReceiveCustomerInfoCallback {
            override fun onReceived(customerInfo: CustomerInfo) {
                val unlocked = applyCustomerInfo(customerInfo)
                callback(
                    PremiumActionResult(
                        ok = true,
                        unlocked = unlocked,
                        message = if (unlocked) {
                            "Benchmark Lab purchase restored"
                        } else {
                            "Restore completed; benchmark_lab entitlement is not active for this Play account"
                        },
                    )
                )
            }

            override fun onError(error: PurchasesError) {
                callback(
                    PremiumActionResult(
                        ok = false,
                        unlocked = benchmarkLabUnlocked,
                        message = "Restore failed: ${error.message}",
                    )
                )
            }
        })
    }
}
