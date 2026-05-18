curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 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" \
  -d '{
    "model": "gpt-5.4-mini",
    "input": "write a haiku about ai",
    "store": true
  }'