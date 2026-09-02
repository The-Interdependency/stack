package org.interdependency.ahbg

import android.content.Context
import com.revenuecat.purchases.CustomerInfo
import com.revenuecat.purchases.Purchases
import com.revenuecat.purchases.PurchasesError
import com.revenuecat.purchases.PurchasesConfiguration
import com.revenuecat.purchases.interfaces.ReceiveCustomerInfoCallback

/**
 * One clean entitlement: `benchmark_lab`.
 *
 * Basic gameplay and external harness connectivity are always free. Benchmark
 * Lab (advanced scenarios, saved/replayed run comparison, adversarial packs)
 * unlocks only when RevenueCat reports the `benchmark_lab` entitlement as
 * active for the current app user.
 *
 * RevenueCat 10.x with the `purchases-store-galaxy` billing backend: the
 * store (Galaxy, or a later Play build with its module added) is auto-detected
 * at runtime, so this file never hard-codes a store.
 *
 * When the RevenueCat key is not provisioned (free/dev builds), the store
 * degrades to the free tier rather than crashing or faking premium.
 */
interface PremiumStore {
    fun isBenchmarkLabUnlocked(): Boolean

    companion object {
        const val ENTITLEMENT = "benchmark_lab"

        fun create(context: Context, revenueCatApiKey: String): PremiumStore {
            return if (revenueCatApiKey.isBlank() || revenueCatApiKey.startsWith("REVENUECAT_KEY_NOT_PROVISIONED")) {
                NoopPremiumStore()
            } else {
                RevenueCatPremiumStore(context, revenueCatApiKey)
            }
        }
    }
}

class NoopPremiumStore : PremiumStore {
    override fun isBenchmarkLabUnlocked(): Boolean = false
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
        Purchases.sharedInstance.getCustomerInfo(object : ReceiveCustomerInfoCallback {
            override fun onReceived(customerInfo: CustomerInfo) {
                benchmarkLabUnlocked =
                    customerInfo.entitlements.active[PremiumStore.ENTITLEMENT]?.isActive == true
            }

            override fun onError(error: PurchasesError) {
                benchmarkLabUnlocked = false
            }
        })
    }

    override fun isBenchmarkLabUnlocked(): Boolean = benchmarkLabUnlocked
}
