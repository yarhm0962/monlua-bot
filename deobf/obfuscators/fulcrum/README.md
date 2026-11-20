# Fulcrum Deobfuscator integration

The detector recognizes the exact archived reference fingerprint and corroborated Fulcrum VM structure. It also excludes the archived Luraph control fingerprint.

The uploaded archive does not contain the raw reference inputs. Its main two-stage engine imports tool.py and lualex.py from absolute paths that are not included. The standalone package scanner documents that its recovered strings are unverified candidates and that it is not a VM devirtualizer.

For these reasons, the bot registers Fulcrum detection but keeps the recovery option disabled. It does not present partial string candidates as deobfuscated source. Full recovery should only be enabled after the missing dependencies and authorized reference input are supplied and the output is validated against the original behavior.
