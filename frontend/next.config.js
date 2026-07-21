/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  // Since GitHub pages hosts at <username>.github.io/<repo-name>, 
  // we check if it is being built in GitHub Actions to append the repository path.
  basePath: process.env.GITHUB_ACTIONS ? '/KALKI-1.5' : '',
}

module.exports = nextConfig
