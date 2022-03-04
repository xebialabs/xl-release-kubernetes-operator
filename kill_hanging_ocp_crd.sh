kubectl patch digitalaireleaseocps.xlrocp.digital.ai/dai-ocp-xlr \
  --type=merge \
  --patch '{"metadata":{"finalizers":[]}}'
