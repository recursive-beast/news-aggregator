FROM n8nio/n8n:latest

USER root

RUN set -e; \
    SCOPES_FILE=$(find /usr/local/lib/node_modules/n8n -name "global-scopes.ee.js" | head -n 1) && \
    [ -n "$SCOPES_FILE" ] && \
    sed -i "/exports.GLOBAL_MEMBER_SCOPES = \[/a\    'user:create'," "$SCOPES_FILE" && \
    sed -i "/exports.GLOBAL_MEMBER_SCOPES = \[/a\    'user:changeRole'," "$SCOPES_FILE" && \
    sed -i "/exports.GLOBAL_CHAT_USER_SCOPES = \[/a\    'user:create'," "$SCOPES_FILE" && \
    sed -i "/exports.GLOBAL_CHAT_USER_SCOPES = \[/a\    'user:changeRole'," "$SCOPES_FILE" && \
    LICENSE_FILE="/usr/local/lib/node_modules/n8n/dist/license.js" && \
    [ -f "$LICENSE_FILE" ] && \
    sed -i 's/return this\.manager?.hasFeatureEnabled(feature) ?? false;/return true;/' "$LICENSE_FILE" && \
    sed -i 's/return this\.isLicensed(feature);/return true;/' "$LICENSE_FILE" && \
    sed -i 's/return this.getUsersLimit() === constants_1.UNLIMITED_LICENSE_QUOTA;/return true;/' "$LICENSE_FILE" && \
    sed -i 's/if (!this.isLicensed())/if (false)/' "$LICENSE_FILE"

# Switch back to the n8n user to avoid running the application as root
USER node
