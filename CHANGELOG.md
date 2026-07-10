# Changelog

## [0.3.0](https://github.com/junox-systems/wagtail-starter-kit/compare/v0.2.2...v0.3.0) (2026-07-10)


### Features

* cache by default in pages ([5c8b3bd](https://github.com/junox-systems/wagtail-starter-kit/commit/5c8b3bdaf2e8be85426fe6714552663e88e7d45b))
* modular settings, rm sqlite cache ([65f2f92](https://github.com/junox-systems/wagtail-starter-kit/commit/65f2f92b61ec864b9471d46fbfe98e902f80342e))
* upgrade vite to v8 ([06444b8](https://github.com/junox-systems/wagtail-starter-kit/commit/06444b87aa443a67a4db23b722e220f4b35df1d3))


### Bug Fixes

* sorting in items in pages ([8c50300](https://github.com/junox-systems/wagtail-starter-kit/commit/8c503004780a9a3bc960ebe0e1030c29f33f9b82))
* treebeard version error ([f631dae](https://github.com/junox-systems/wagtail-starter-kit/commit/f631dae88c50c62bfe75ce0de5c6e1ac81dcdc82))
* use default dev django server ([945e981](https://github.com/junox-systems/wagtail-starter-kit/commit/945e981b35084030a1e6ee26eeeab8cce9ef52cf))

## [0.2.2](https://github.com/junoxlabs/wagtail-starter-kit/compare/v0.2.1...v0.2.2) (2025-10-09)


### Bug Fixes

* env file sample for prod ([8db8f97](https://github.com/junoxlabs/wagtail-starter-kit/commit/8db8f972d6fdef54aa8f7bbc4e75f3cc71dc8c4a))
* move Dockerfile to root dir ([d2c7b83](https://github.com/junoxlabs/wagtail-starter-kit/commit/d2c7b83d64ad69c1e2729ebad24ef5bdf94395e4))
* prod Dockerfile works ([e1b24f4](https://github.com/junoxlabs/wagtail-starter-kit/commit/e1b24f4f32a207f85b7e8e2bec9e9a00d78ea631))
* use almalinux 9; 10 doesn't support older cpu ([aa230b3](https://github.com/junoxlabs/wagtail-starter-kit/commit/aa230b31270f403663b8d0f0a96fb9ab819ca46f))

## [0.2.1](https://github.com/junoxlabs/wagtail-starter-kit/compare/v0.2.0...v0.2.1) (2025-09-29)


### Bug Fixes

* app name / site title not showing in frontend ([4b467b4](https://github.com/junoxlabs/wagtail-starter-kit/commit/4b467b40e8c9c1e7ce7d1f75ec362723804a7158))
* nav/menu admin menu; consistent animations ([a39ad62](https://github.com/junoxlabs/wagtail-starter-kit/commit/a39ad626e5bc02b5384627c384fa7b8ac3b8e211))
* outdated docs / README ([eb92339](https://github.com/junoxlabs/wagtail-starter-kit/commit/eb923395b873f73445865c81c422237839153e00))

## [0.2.0](https://github.com/junoxlabs/wagtail-starter-kit/compare/v0.1.0...v0.2.0) (2025-09-24)


### Features

* add hotwire turbo ([dead2ef](https://github.com/junoxlabs/wagtail-starter-kit/commit/dead2ef32f81b50b48987e2aeb4644cfde9e3c0c))
* config security env vars ([2dca75c](https://github.com/junoxlabs/wagtail-starter-kit/commit/2dca75c4f43fd7967293cf716b477e28ef1d1c88))
* docker compose based dev environment ([3f1864e](https://github.com/junoxlabs/wagtail-starter-kit/commit/3f1864e955614172c2f9965dc7a741710f5a7852))
* migrate to vite from webpack ([b368df9](https://github.com/junoxlabs/wagtail-starter-kit/commit/b368df9249b578b22ab782b39ae812c09b1126ec))
* rm htmx; move to stimulus + turbo for forms ([9a9a366](https://github.com/junoxlabs/wagtail-starter-kit/commit/9a9a3660fee92585a3c649680b7f4445082ff435))
* s3 for wagtail media; works with minio in dev ([47fe036](https://github.com/junoxlabs/wagtail-starter-kit/commit/47fe036dfaac74fce764496ea8ff07ecc794b678))
* showcase_page init agentic ([af60988](https://github.com/junoxlabs/wagtail-starter-kit/commit/af6098819b278ff712dea6d0385a80d910bd543c))
* use granian over gunicorn ([d39d0f0](https://github.com/junoxlabs/wagtail-starter-kit/commit/d39d0f08059b08561ce30d3ab3947e373601d283))
* use sqlite, litestream ([e2da8ec](https://github.com/junoxlabs/wagtail-starter-kit/commit/e2da8ecc1bff5b90171ac2f74deec87016b97a05))
* working showcase pages ([9e7aa37](https://github.com/junoxlabs/wagtail-starter-kit/commit/9e7aa376ea5a38dc1171898d751c8d9b6866e593))


### Bug Fixes

* add DEBUG=true on dev compose ([f3d236f](https://github.com/junoxlabs/wagtail-starter-kit/commit/f3d236f5b37efa13d66f67fa54dc36017b991547))
* Dockerfile builds; working css. ([fae3757](https://github.com/junoxlabs/wagtail-starter-kit/commit/fae3757b88876c27336aa8e7530e991162845a0d))
* js in head tag w/ defer ([305d5fa](https://github.com/junoxlabs/wagtail-starter-kit/commit/305d5fa144049c41b1a07b7e062b802050f633f0))
* rm duplicate uuid field ([28355d8](https://github.com/junoxlabs/wagtail-starter-kit/commit/28355d81efd721f1b08c917b3505bf7057d4d5a2))

## 0.1.0 (2025-08-11)


### Features

* add GSAP 3 in the frontend mix ([24d122b](https://github.com/junoxlabs/wagtail-starter-kit/commit/24d122b0922aca877b2d8444f9887ccd1ec6813b))
* add synthwave theme as default, dark. ([e0ea83b](https://github.com/junoxlabs/wagtail-starter-kit/commit/e0ea83b1c78836e5369f6c997c3825fab6b9553c))
* add tailwind typography plugin ([50119bb](https://github.com/junoxlabs/wagtail-starter-kit/commit/50119bb6aaafa98a431bc82dbcb4b73d15b200f2))
* add uuid to basepage ([a574b7a](https://github.com/junoxlabs/wagtail-starter-kit/commit/a574b7a428aa52d6ff197df056b80e9a7a80b810))
* forms works ([e471c3d](https://github.com/junoxlabs/wagtail-starter-kit/commit/e471c3dbcedde36c5f859802b369edb09af23384))
* multiple types of hero sections; table_block ([e51f804](https://github.com/junoxlabs/wagtail-starter-kit/commit/e51f804962d8de18c9288585c7329f5c456e714e))
* navigation ([5c3a0bc](https://github.com/junoxlabs/wagtail-starter-kit/commit/5c3a0bc13479c8c2abe56fe2acac23153f2a715b))
* responsive navbar w/ smooth animation ([3fb9373](https://github.com/junoxlabs/wagtail-starter-kit/commit/3fb9373aa50ed1be09056590b1c2b7d8c9b32cb4))
* seo app is now settings ([ac8ee4e](https://github.com/junoxlabs/wagtail-starter-kit/commit/ac8ee4e2acd4309791db0c3a9ee4b0f29ca1e52e))
* unify standard, home pages into FlexPage ([56a2edb](https://github.com/junoxlabs/wagtail-starter-kit/commit/56a2edb9b46c2fc5305aea2f97326ec2c2fef350))
* use pre-commit-hooks to fmt, lint; Dockerfile ([5122b8c](https://github.com/junoxlabs/wagtail-starter-kit/commit/5122b8c92393faa7705413542960c49e912a0f0c))
* wagtail starter kit 0.0.1 init ([5a589f1](https://github.com/junoxlabs/wagtail-starter-kit/commit/5a589f1a8c4bccd8f72d689d3bed4c9dea9aaeef))
* working snippets, blocks, forms, htmx ([609553f](https://github.com/junoxlabs/wagtail-starter-kit/commit/609553fd9a3db034805648248bfe023fd3e6c632))


### Bug Fixes

* forms page_id error ([53824dc](https://github.com/junoxlabs/wagtail-starter-kit/commit/53824dcd71f662bd57cfdb6deb4a2e3a35f838ad))
* homepage; css; js works ([2704da8](https://github.com/junoxlabs/wagtail-starter-kit/commit/2704da88a9a5cf4ff8fad7dfe3835cb8e37863f3))
* rm dual page templates; unify ([bc06f77](https://github.com/junoxlabs/wagtail-starter-kit/commit/bc06f77dc0abc5dc7076b309cf6f1412de1dd8b8))
* tailwind v4 JIT compiler ([c155a0a](https://github.com/junoxlabs/wagtail-starter-kit/commit/c155a0ae95d226b0b01ea8a28de0a12a755d7819))
* use defer for javascript ([11ee9b0](https://github.com/junoxlabs/wagtail-starter-kit/commit/11ee9b05993d0e9a10bc64c47eb5dd4cf3d0e38e))
* working forms w/ htmx ([015f21f](https://github.com/junoxlabs/wagtail-starter-kit/commit/015f21f46f96c0def4d0723b09b02a7ba194771d))
