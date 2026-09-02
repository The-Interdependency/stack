plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "org.interdependency.ahbg"
    compileSdk = 35

    defaultConfig {
        applicationId = "org.interdependency.ahbg"
        minSdk = 26
        targetSdk = 35
        versionCode = 2
        versionName = "0.2.0"
        // Production runtime endpoint. Release builds must use HTTPS; debug
        // builds may point at a local emulator host through
        // -PruntimeUrl=http://10.0.2.2:8765. The mobile layer never embeds
        // the engine itself.
        val runtimeUrl = (project.findProperty("runtimeUrl") as String?) ?: "https://ahbg.interdependentway.org"
        buildConfigField("String", "RUNTIME_URL", "\"$runtimeUrl\"")
        // RevenueCat public API key. Provisioned at build time; never committed.
        val revenueCatKey = (project.findProperty("revenueCatApiKey") as String?) ?: "REVENUECAT_KEY_NOT_PROVISIONED"
        buildConfigField("String", "REVENUECAT_API_KEY", "\"$revenueCatKey\"")
    }

    signingConfigs {
        create("release") {
            val storeFilePath = (project.findProperty("ahbgStoreFile") as String?).orEmpty()
            if (storeFilePath.isNotEmpty()) {
                storeFile = file(storeFilePath)
                storePassword = project.findProperty("ahbgStorePassword") as String?
                keyAlias = project.findProperty("ahbgKeyAlias") as String?
                keyPassword = project.findProperty("ahbgKeyPassword") as String?
            }
        }
    }

    buildTypes {
        debug {
            // Emulator/localhost cleartext only; controlled by network security config.
        }
        release {
            isMinifyEnabled = false
            if ((project.findProperty("ahbgStoreFile") as String?).isNullOrEmpty().not()) {
                signingConfig = signingConfigs.getByName("release")
            }
        }
    }
    buildFeatures {
        buildConfig = true
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.webkit:webkit:1.12.1")
    implementation("com.revenuecat.purchases:purchases:8.10.1")
}
