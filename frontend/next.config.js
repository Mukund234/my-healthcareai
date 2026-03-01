const nextConfig = {
    output: 'export',
    basePath: '/my-healthcareai',
    assetPrefix: '/my-healthcareai/', // Explicitly set for GitHub Pages
    trailingSlash: true,
    images: {
        unoptimized: true,
    },
    env: {
        NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    },
}

module.exports = nextConfig
