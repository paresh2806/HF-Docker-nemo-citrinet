## 🎯 Example: Transcribe Audio via API

```bash
curl --location 'https://{organization}-{spacename}.hf.space/transcribe/' \
--header 'Authorization: Bearer XXXXXXXXhuggingfaceXXXXXXXXXXXXXXX' \
--form 'file=@"/home/paresh/Data/Test-Audio/OSR_uk_000_0049_8k.wav"'
