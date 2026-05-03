/**
 * Swarm Enterprise OS - Global Configuration
 * Centralized endpoint management for the Sovereign SDK.
 */

const Config = {
    // Primary API Gateway - Points to your Cloudflare-protected domain
    API_BASE_URL: "https://corp.realms2riches.com/api",
    
    // Output Viewer Gateway - Where the customer sees their code
    VIEWER_URL: "https://viewer.realms2riches.com",
    
    // WebSocket / Real-time Log Stream (Reserved for Supervisor Tier expansion)
    WS_URL: "wss://corp.realms2riches.com/ws",

    // UI Metadata from brand_assets.json (Matches File #11)
    VERSION: "1.0.0",
    DEBUG_MODE: false,

    /**
     * getEnv: Safely retrieves current environment context.
     * Prevents the app from choking if the tunnel is momentarily down.
     */
    getEnv: () => {
        return {
            isProduction: window.location.hostname !== "localhost",
            currentHost: window.location.host,
            timestamp: new Date().toISOString()
        };
    }
};

export default Config;