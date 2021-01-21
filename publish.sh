cd client/src
npm run build
env CF_ACCOUNT_ID=`cat .cf_account_id` wrangler publish
