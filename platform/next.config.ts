import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    // PPR is not yet stable, disabling for now
    // ppr: true,
  },
  images: {
    remotePatterns: [
      {
        hostname: "avatar.vercel.sh",
      },
    ],
  },
};

export default nextConfig;
