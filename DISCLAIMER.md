# Disclaimer & License

## Disclaimer

SiftBlock's output blocklist is provided **as-is**, without warranty of any kind. It is compiled automatically from publicly available threat intelligence sources, filtered down to domains matching the keywords configured in `config/keywords.txt`.

- Domains are added based on their appearance in upstream sources — no manual verification is performed.
- Legitimate domains may occasionally be included (false positives). If you believe a domain has been listed in error, please [open an issue](../../issues).
- These lists are intended to supplement, not replace, a full security solution.
- The maintainers of this project are not responsible for any damage, data loss, or disruption caused by its use.

## Sources

SiftBlock aggregates data from the following third-party sources (see `config/sources.txt` for the exact feed URLs in use), each with their own terms:

- [HaGeZi DNS Blocklists](https://github.com/hagezi/dns-blocklists)
- [BlocklistProject](https://github.com/blocklistproject/Lists)
- [NoTracking Hosts Blocklists](https://github.com/notracking/hosts-blocklists)
- [Phishing.Database by mitchellkrogza](https://github.com/mitchellkrogza/Phishing.Database)
- [UT1 Blacklists](https://github.com/olbat/ut1-blacklists)
- [Maltrail by stamparm](https://github.com/stamparm/maltrail)
- [Ultimate Hosts Blacklist](https://github.com/Ultimate-Hosts-Blacklist/MalwareDomainList.com)
- [StevenBlack Hosts](https://github.com/StevenBlack/hosts)

Credit goes entirely to the maintainers of those projects.

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
