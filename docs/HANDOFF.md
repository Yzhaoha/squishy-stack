# 捏捏叠叠乐 Squishy Stack · 交接（给 Claude Code）

更新：2026-11-21。全程中文回复；用户不看代码，只看效果，说话直白。

# 先读这里（11-21 交接，下面旧内容是逐日记录，要查细节再翻）

## 一句话现状
美术、内容量、音乐、标题页、CrazyGames 包、预览视频、表单文字都做完了，**但用户和我都认为核心玩法不好玩**（「只是往上叠」「太简单」）。备用位、按住捏紧两次改操作的尝试用户都说没区别。**用户最新指示：做两个原型给他玩了再定——①真物理叠塔 ②合成（同款碰到合成更大的）。原型还没写，只准备了物理引擎。还没投 CrazyGames，先别投。**

## 11-24 晚：参考羊了个羊规则的合成玩法（proto-pile.html，等用户试玩）
- 用户要求：参考羊了个羊（第一关简单、第二关特别难），但仍然是合成。方案「捏捏罐子大挑战」：罐子预先塞满物理堆，只能点露在最上面的（上面压着的变暗，判定见 cover()），点了进 7 格托盘；托盘 3 只同款 → 捏成大一级掉回罐子；到 cap 级凑 3 只就「毕业」飞走。托盘满输，罐子 + 托盘 + 暂存全清赢。盲盒纸（wrap）露出来才揭晓。
- 道具每关各 1 次 + 「再领一次」（正式版看广告）：捏一下（震乱重堆）、移出（托盘 3 只到暂存，点暂存的放回托盘）、撤回；托盘满可复活一次（挪出 3 只）。
- 关卡由 genPile 生成且必定有解：从 G 组 cap 级三连开始，反复把一只拆成 3 只低一级；种子固定（每次同一堆）。第 1 关 cap2 13 只；第 2 关 cap8 G2 99 只、盲盒 70%、尺寸 ×0.8。
- 机器人（贪心）：第 1 关 5/5；第 2 关不用道具 0/10，用全道具 + 复活约 1/16。
- 生成：`python3 tools/build_protos.py`（模板 tools/proto/pile.tpl.html），测试钩子 `window.__g`。

## 11-24：用户选了合成，原型扩成试玩版（proto-merge.html）
- 用户试玩后：「合成的更好玩」，但嫌乱 → 加了「回正」（每帧把角速度拉回趴姿）、合成链按颜色错开：麻薯→包子→青蛙→草莓→柴犬→果冻→企鹅→小熊→独角兽→巨型水豚，宽 46→240。
- 用户同意的设计：①自己的核心操作「捏一下」②主模式改关卡，每章一个新东西（1 基础 2 彩虹 3 冰冻 4 罐子变形 5 泡泡/蜂蜜）+ 无尽 ③搬现有图鉴/盲盒/商店。先做试玩版给用户玩，再铺 50 关。
- 试玩版已做：选关界面、3 关 + 无尽。「捏一下」= 罐子上方按钮（或 S 键）进入捏模式，再点一只：缩到 0.75 再弹回、推开周围、往上跳；捏冰块敲掉一层冰；每合成 5 次 +1，最多 5。第 1 关合出柴犬；第 2 关彩虹捏捏（RB=-1，圆形，碰谁谁升一级），合出小熊；第 3 关 4 只冰冻（静态，旁边合成或捏一下各敲一层，2 层），25 只以内（L.limit，「还剩 N 只」）。
- 机器人乱扔通过率：第 1 关 8/8（约 9 只），第 2 关 8/8（约 35 只），第 3 关 6/8，会用捏一下时 8/8。
- 进度存 localStorage `sqp_mergeDone` / `sqp_mergeBest`。测试钩子 `window.__m`（start(i)、step、squeeze(b)、setAim、drop）。
- **等用户试玩反馈**，再决定铺 50 关并搬进 index.html。

## 11-21 晚：两个原型已做完（等用户试玩）
- `proto-physics.html` / `proto-merge.html` 在仓库根目录，由 `python3 tools/build_protos.py` 从 `tools/proto/*.tpl.html` 生成（内嵌 Matter.js、角色图、碰撞轮廓）。改模板后重跑。
- 物理叠塔调过的参数：放下直落（不带吊钩速度）；碰撞轮廓往方框收 50%（BOXK）；落地后转动阻尼 ×0.8/帧（ANGD）；每帧物理拆 3 小步（SUB=3，不拆的话高塔底部会被慢慢挤出去）。关卡：底座 300/230/180，目标 230/300/340。机器人（对准塔顶中心、误差 ±15）过关率约 7/8、4/8、1/8。
- 合成：随机乱扔的机器人能合到第 9 级「小龙」。
- 测试钩子：`window.__p`（物理）、`window.__m`（合成），都有 step()。
- 已推到开发分支 `claude/adoring-fermat-htrw6s`；推 main 需要用户在本次会话同意。

## （原计划）两个原型
用户原话：「你一和三都做一个，我看看吧」。各做一个**独立小页面**放仓库根目录（Pages 会直接发布），不要动 index.html：
- `proto-physics.html`：真物理叠塔。吊钩左右荡，点一下放下；每只捏捏是有形状有重量的刚体，放歪会滑、圆顶上会滚、会连带倒。目标是塔顶够到一条高度线并稳住 1 秒多；掉下去 3 只算输。3 关，底座一关比一关窄。选形状差别大的角色：shiba、bun（圆顶）、toast（方）、boba / mush（高）、cro / shark（扁宽）、pud。
- `proto-merge.html`：合成。竖着的容器，移动瞄准、松手落下；两只同款碰到合成下一级更大的，堆过警戒线 2 秒算输；有分数和最高分。建议的合成链（由小到大）：mochi → bun → frog → shiba → cat → bear → sloth → uni → dragon → gcapy，宽度约 50→220。只随机掉前 5 级。
- 已准备：`tools/proto/matter.min.js`（Matter.js 0.19.0，MIT 许可，要**内嵌**进页面，不能外链）。
- 设想的做法（还没写）：写 `tools/build_protos.py`，从 `art/characters/*.png` 的透明轮廓算每只的凸包（十来个顶点，按裁边后图宽归一化），连同 index.html 里 `/*ART*/` 的图和 `/*PROPS*/` 的背景一起注入模板。Matter 的 `Bodies.fromVertices` 会把顶点重新对到质心，画图时要按质心偏移。碰撞时给一个只影响显示的压扁弹簧，保住「捏」的手感。
- 做完给两个链接：`https://yzhaoha.github.io/squishy-stack/proto-physics.html?v=N` 和 `proto-merge.html?v=N`，让用户各玩几分钟。哪个好玩就把现有美术、盲盒、图鉴、关卡界面搬过去；都不好玩再议。
- 教训：**别再在现有玩法上贴功能**。用户否掉的：下一只预览、备用位（「又不是俄罗斯方块」）、按住捏紧（「核心玩法没有什么区别」）。

## 游戏现在有什么（index.html，v6.3，单文件约 1.07MB）
- 50 关 5 章 + 无尽模式；34 只角色全部正式图（新的粉嫩风格），背景 3 张、金币、小蓝鸟、底座、3 个盲盒也是图。
- 机制：风、飞鸟、空中金币（含金币关）、滑动底座、弹弹云、忽明忽暗、冰面打滑、吊钩忽快忽慢、巨型捏捏、捏捏狂热（连 3 次完美）、同款三连奖励。
- 「捏」手感：落地压扁回弹、压力波下传、被压着变扁、塔像果冻一样歪、晃时冒汗发抖。
- 图鉴里的捏捏玩具、盲盒、商店、签到、任务、对手排行榜；11 语言；合成的背景音乐和音效。
- **v6.3 的「按住捏紧」是试验版，用户说没区别，建议去掉**（删 sqStart / sqEnd / sqTick、drop 的 charge 参数、G.sq、文案 tipSq / sqz，或者默认关掉）。链接加 `?sq=0` 是旧的一键操作。

## 链接和文件
- 测试链接：https://yzhaoha.github.io/squishy-stack/ （main 分支根目录；给用户的链接加 `?v=N`，上一个用到 65）。开发分支 `claude/clever-sagan-668py9`，每次都同时推到 main（用户 11-18 同意过）。
- `tools/embed_art.py`：把 `art/characters/` 的图裁边、压 WebP、写进 index.html 的 `/*ART*/` 和 `/*PROPS*/`。新图放进去再跑一次。
- `tools/build_cg.py` → `dist/squishy-stack-crazygames.zip`（改了 index.html 要重跑）。`tools/make-video.js` → `submission/preview-*.mp4`。`submission/表单文字-CrazyGames.md`。
- `docs/art-todo.md`：给用户本机会话的画图清单（末尾有 3 张封面的提示词）。
- 测试钩子 `window.__sq`（只在测试版）；快速模拟：循环 `__sq.step(1/60)`，pick 状态调 `__sq.choose(0)`。注意 `CH` 是画面高度，章节表叫 `CHAP`。

## 美术还缺的
- capy / dump / axo 仍是旧风格，和其他 31 只不是一套（用户本机会话在 ChatGPT 里重画，文件名不变覆盖上传）。
- 封面 3 张（没画）；第 4、5 章没有专门背景（现在是旧背景加色调）；7 个底座皮肤和界面图标仍是代码画 / emoji；电脑横屏背景是竖图放大，偏糊。
- 画图只能在用户本机做：云端会话连不上用户电脑（「claude美术」文件夹显示 not_available），也没有操作浏览器的工具。本机会话在 `D:\claude美术\squishy-stack`，那台电脑没装 git，图是网页上传的。

## CrazyGames
- **这个游戏没投过 CG**（只在 11-13 投过 Poki，11-14 模板信拒）。用户曾以为投过，按文档没有，建议让用户在 CG 后台确认。
- 用户的 Pogo Post 11-20 过审进试运行（公开仓库 `Yzhaoha/pogo-post`，读它的 docs/STATUS.md）。它是代码画的画面但有 90 关 9 章、每跳两个操作。结论：审核看完成度，留存看玩法。
- 提交用哪个账号由用户定（Stone Tech，或 Pogo Post 用的 QQ 邮箱那个）。

## 用户规矩（一直有效）
- 测试链接一律 GitHub Pages。**提交表单永远不选任何 AI 相关选项**；若单独问是否用 AI 生成内容，停下来问用户。
- 不替用户注册、不输密码；确认框用户自己勾；最终提交前截图给用户确认。用户邮箱是隐私。
- 用户会反复问「跟线上游戏比还差什么」「好不好玩」：要直说，不要客套。他的直觉（太简单、只是往上叠）一直是对的。
- 长时间闷头干活他会不耐烦，隔一会儿说一句在做什么。

---

# 以下是旧记录（11-17 起，按时间顺序）

## 用户规矩
- 测试链接一律用 GitHub Pages：https://yzhaoha.github.io/squishy-stack/ （本仓库根目录 index.html = 测试版；`_config.yml` 排除了 poki/ tools/ docs/）
- **提交表单永远不选任何 AI 相关选项**（引擎 / Tools 不填 Claude、ChatGPT、AI）。
- 不替用户注册账号、不输密码，需要登录喊用户；确认框由用户自己勾；最终提交前先截图给用户确认。
- 用户邮箱是隐私，不发给外部服务。

## 现在的状态
- 本仓库 `index.html` = **v5.1**（11-14）：在 v5 基础上加了 Esc/P 暂停、广告期间挡操作、Poki 构建脚本 `tools/build_poki.py`（输出 poki/index.html 和 build/squishy-stack-poki.zip）。
- **Poki：11-13 提交，11-14 收到模板拒信**（「暂时不给 Poki for Developers 抢先体验资格，测试名额有限」，没提游戏问题；Poki 对用户其他游戏也是同一封信）。→ 不再为 Poki 独占，**改投 CrazyGames**。
- CrazyGames 已经用「The overall quality of the game does not yet meet the expectations of our platform」通用理由拒了用户 5 次（怪物糖果夜 ×2、坑勇者、劫匪大乱斗、坑前男友）。
- CG 提交身份：nc8020503@gmail.com / 开发者名 **Stone Tech**（同一账号同时只能有一个游戏在等审核；Stone Tech 还要送审 Burnt Again 草稿，顺序问用户）。

## CG 同类对比（11-16）
CG 上没有「吊钩叠塔」直接竞品。最接近的：
- Stacky Bird（Kooapps，8.6 分、3.4 万赞）：一键叠蛋；3 连完美进射击模式；世界地图 + 剧情；金币装修小屋；日/周/总榜；限时活动。
- Hit the Stack（2026-10 上线，9.0）：3D 物理、手工关卡、金币、道具、收集物。
- Sketchy Towers（8.4）：物理叠塔，掉 5 块输，同色加分，多地图，排行榜。
- Blast Stack（9.0，Unity 6）：画面精致的解谜。
**最大风险：我们的角色是代码画的。**

## 改进计划（按优先级）
1. **换正式美术**：ChatGPT 画 34 只捏捏 + 3 背景 + 3 盲盒。提示词和规格见 `docs/chatgpt-art-prompts.md`。
2. **真正的「捏」手感**：落下压扁回弹、被上面压着微微变形、晃塔时冒汗发抖（不再画代码脸）、倒塌时软软滚落。
3. 连续完美奖励模式（如 3 连完美进「捏捏狂热」：几秒自动对正、金币翻倍、背景变色）。
4. 收藏展示柜（抽到的捏捏摆出来看）。
5. 排行榜：现在是 24 个程序生成的「对手捏捏」（不冒充真人）；CG 官方排行榜只给受邀游戏（SDK `user.submitScore` + 加密密钥）。
6. 关卡目标多样化（指定系列、碰空中金币、躲飞鸟）。
7. CG 版：新写 `tools/build_cg.py`（CG SDK v3 + Data 模块存档 + muteAudio + midgame/rewarded，接口跟 Poki 版的包装层一致）；封面 3 张（1920×1080 / 800×1200 / 800×800）；预览视频横 1920×1080 + 竖 1080×1620，15–20 秒、无声、第一帧是封面；手机竖屏重点优化。CG 里 Esc 是浏览器保留键，暂停用 P。

## 美术进度（重要）
- 在用户 yzhao185 那个 Chrome 的 ChatGPT（Plus）里，对话「Generate Capybara Image」（chatgpt.com/c/6afab9af-1c78-83e8-a2db-b3249059090f）已画好 **水豚 capy、饺子 dump、六角恐龙 axo** 三张，风格统一（软亮捏捏质感、黑豆眼、腮红、扁宽）。
- **三张原图已放进本仓库 `art/characters/`**：capy.png、dump.png、axo.png（1536×1024，都是真透明背景 RGBA；可见部分宽高比约 1.79 / 1.88 / 1.93，四周有空边要裁掉；边缘有淡淡半透明，裁边时用 alpha>40 判断）。
- 剩下 31 只继续在**同一个 ChatGPT 对话**里画，每次开头说 "Same style, lighting, face and canvas as the capybara"。

## v5.2（11-18，分支 claude/clever-sagan-668py9）
- 水豚、饺子、六角恐龙三张图已内嵌（`tools/embed_art.py`：裁边、找身体框和眼睛、压成 WebP，写进 index.html 的 `/*ART*/…/*ENDART*/`）。新图放进 `art/characters/<id>.png` 再跑一次脚本即可；身体框不准时在脚本的 OVERRIDE 里手调，`--debug 目录` 可出检查图。没图的角色仍是代码画法。
- 「捏」手感：落下压扁回弹（按下落速度，压力像波一样往下传）、下落时拉长、被上面压着变扁变宽（p.c，最多 10%，塔高按压扁后的高度算）、塔晃时像果冻一样倾斜 + 冒汗发抖。有图的角色不再画代码脸，只叠加眨眼、汗滴、星星。
- 11-18 用户确认图可以 → 用户去画剩下 31 只。
- v5.3：标题页回来后重新摆展示塔（宽屏挪到面板左边）；加了「捏捏狂热」（狂热外连续 3 次完美触发，7 秒内每次落下自动对正、金币 ×2、彩虹背景；G.fever / G.fevN / FEVER_T，文案键 fever）。
- v5.4：空中金币（G.airs，下落时碰到 +5；关卡 `gold:n` = 还要接住 n 个才过关，第 3/6/8/12/14/17/22/25/27 关）、飞鸟（G.birds，撞到会把下落的捏捏撞偏；关卡 `birds`，无尽 12 层起）、图鉴点已拥有的角色打开「捏捏玩具」（可以一直点着捏）。文案键 r_gold / r_birds / poke。飞鸟是代码画的，以后可换图。
- v5.5（用户觉得「只是往上叠太简单」）：备用位（#holdB，A / Shift 或点按钮，每次落下前只能换一次；G.hold / swapHold）+ 下一只预览（#nextB）；同款三连（连着 3 只同款：+12 金币、塔晃动 ×0.35、打星标；G.tri）；每关固定 4 只阵容（L.cast，开始界面会显示）；关卡 `tri:n` = 要做 n 次三连才过关（第 2/11/16/21/29 关）。文案键 hold / triple / r_tri。
- v5.6：用户说备用位和下一只预览都没用（「又不是俄罗斯方块」）→ 都删了，三连关（tri 过关条件）也取消。保留：同款三连奖励（纯运气奖励）、每关 4 只阵容。**教训：这游戏靠手感和时机，别加规划类玩法。**
- 11-20：对比线上游戏后定的补齐顺序：①美术全换（31 只 + 鸟/金币/底座 + 3 背景 + 3 盲盒，用户照 `docs/art-todo.md` 在 ChatGPT 里画，传到 art/characters/）②背景音乐和像样音效 ③真正不同的关卡（移动底座、变窄）④标题页重做。这个游戏还没投过 CrazyGames，补完再投。

## 美术进度 11-20（本机会话在 D:\claude美术\squishy-stack 用 Chrome 里的 ChatGPT 画）
- **风格改了**：用户要求「更粉嫩可爱」——粉彩暖粉色调、腮红更大更粉、眼睛更大带白色星星高光、身体更圆更胖，保留光泽捏捏质感。提示词开头用 "Generate an image now. Same pinker, cuter style ... as the new pastel ..."，颜色在 art-todo.md 原色上调成粉彩。ChatGPT 已把这条风格写进记忆。
- 萌宠系列 11 只已画完（新风格，透明 PNG）：cow frog shiba rpanda shark peng cat bear sloth dino gcapy。shark 是 1774×887，其余 1536×1024；rpanda 尾巴绕在侧面；dino 背刺黄色略高出背；可见宽高比普遍比目标宽 0.1–0.15。
- **图只在本机，还没进仓库**（那台电脑没装 git）。用网页上传：github.com/yzhaoha/squishy-stack/upload/main/art/characters
- **capy / dump / axo 是旧风格，要按新风格重画**，否则有色差。
- 接下来：甜点 11 只 → 梦幻夜 9 只 → 小物件 → 背景 → 盲盒。图进仓库后跑 `python3 tools/embed_art.py --debug 目录` 检查身体框和眼睛（新风格眼睛带星星高光，眼睛检测可能要调）。
- 11-20 晚：用户网页上传了 22 张新风格图（萌宠 11 + 甜点 11），已嵌入（v5.7，共 25 只有图，index.html 约 690KB）。embed_art.py 改动：关掉眨眼（BLINK=False，新风格大眼睛盖一层不好看）；图和碰撞框比例差超过 4% 时改碰撞高度（ART[id].h，如 boba 80→105、shark 62→47）而不是压扁图。**还缺：梦幻夜 9 只；capy/dump/axo 仍是旧风格待重画；鸟/金币/底座/背景/盲盒。**
- 11-20 夜 v5.8：art-todo 全部画完并入库（43 张）。34 只角色全部有图；道具/背景/盲盒走 embed_art.py 的 PROPS 表 → index.html 的 `/*PROPS*/`，运行时 PIMG[key]：coin（coinIcon）、bird（drawSky）、base（只替换 pink 皮肤，其他 7 个底座皮肤仍是代码画）、box_<系列>（盲盒界面）、bg_<系列>（drawBg：关卡按系列，无尽按高度 pals→cafe→dream 渐变，随镜头从地面滚到天空；有背景时不画代码草地）。index.html 约 1.05MB。**美术只剩：capy/dump/axo 旧风格待重画；7 个底座皮肤、界面 emoji 图标仍非正式美术。**
- v5.9：背景音乐（MUS + musicTick，WebAudio 合成的八音盒循环，8 小节 C–Am–F–G；甜点系列升调、梦幻夜降调放慢、狂热时加速；静音/广告/暂停时停）。落地音效加了回弹尾音。**云端听不到声音，只验证了调度/静音/暂停逻辑，好不好听要用户自己听。** 没用任何音频文件。

## 参考：Pogo Post 过了 CrazyGames 审核（11-19 提交，11-20 通过进 Basic Launch）
公开仓库 `Yzhaoha/pogo-post`，读 `docs/STATUS.md`。它过审时：**画面是代码画的**、单文件 150KB、音乐音效也是代码合成；但有 **90 关 9 章，每章有新机制**（风、风扇、弹床、狗、悬浮平台、冰、雾、雷雨）+ 无尽模式 + 连击计分 + 换装商店 + 11 语言。结论：CG 卡的主要是玩法的深度和变化，不是美术。本游戏现在美术比它强，但 30 关只是数字不同——**优先做每章的新机制**。
可直接借用：`tools/build.py` 里的 CG SDK v3 适配层（把 PokiSDK 形状的接口接到 CrazyGames.SDK，含 muteAudio、locale、midgame/rewarded）、`tools/make-video.js`（预览视频）、`tools/make-covers.js`（封面加字）、`submission/表单文字-CrazyGames.md` 的格式。Pogo Post 用的是「账号 C」（QQ 邮箱，后台 Welcome, Nick），该账号现在没有游戏在等审核。

## v6.0（11-21）：每章的新机制
- 第 2 章 **滑动底座**（L.slide = 幅度，slideOff() 加在 swayAt 里；第 11/13/15/17/19/20 关，第 3 章 25/28 关也有）。
- 第 3 章 **弹弹云**（L.puff，G.puffs，下落的捏捏碰到会弹起一次 +3 金币，横向速度 ×0.2；第 21/23/25/27 关）和 **忽明忽暗**（L.dark，周期变暗只照亮吊钩附近；第 22/24/26/28/30 关）。
- 文案键 r_slide / r_puff / r_dark / boing。机器人（sk=0.06，每关 24 局）通过率：加机制后第 17 关 67%、20 关 50%、25 关 63%、27 关 58%，其余 80%+；第 30 关本来就只有 13–25%。忽明忽暗对机器人无效，实际难度要人玩才知道。
- 快速模拟方法：在页面里循环调 `__sq.step(1/60)`，state==='pick' 时 `__sq.choose(0)`，到 'win'/'end' 结束（不用等真实时间）。

## v6.1（11-21）：标题页重做 + CrazyGames 包
- 标题页：logo 浮在背景上（白字粉描边、轻微浮动）；竖屏时按钮是底部抽屉，展示塔站在抽屉上沿（update 里标题状态镜头目标 = -titleLift()）；横屏仍是居中卡片、塔在左边。展示塔用新风格角色（shiba/bun/frog/…）。#hero 画布已停用。
- `python3 tools/build_cg.py` → `dist/crazygames/index.html` + `dist/squishy-stack-crazygames.zip`（约 730KB）。适配层搬自 Pogo Post：CG SDK v3 → PokiSDK 形状接口；`window.__sqHost.setPlatMute / setLang`（平台静音、按 CG locale 选语言，玩家手选过语言则不覆盖）。假 SDK 验证过调用顺序：init → loadingStart → loadingStop → gameplayStart/Stop，法语 locale 生效。存档只用 localStorage，没接 CG Data 模块（Pogo Post 也没接，过审了）。
- **改了 index.html 之后要重新跑 build_cg.py。**
- 预览视频已录（`node tools/make-video.js`，机器人逐帧录，6 段各 3 秒：飞鸟、狂热、滑动底座、金币、弹弹云、忽明忽暗；`window.__sqManual` 让主循环不自己走）→ `submission/preview-*.mp4`。表单文字在 `submission/表单文字-CrazyGames.md`。
- **还没做：封面 3 张**（提示词在 art-todo.md 末尾，用户本机会话画，存 art/source/；加字和裁成 1920×1080 / 800×1200 / 800×800 的脚本还没写，可搬 Pogo Post 的 make-covers.js）。封面到位后重跑 make-video.js 给视频加封面首帧。

## v6.2（11-21）：第 4、5 章，共 50 关
- 章节表 `CHAP`（注意：`CH` 是画面高度，别重名）。第 4 章「冰雪山顶」第 31–40 关、第 5 章「云端之上」第 41–50 关；这两章角色从全部系列里混着出（L.cast），背景是现有背景加一层色调和雪花/光点（theme: snow / sky），**没有专门的背景图**。
- 新机制：**冰面打滑**（L.ice，落地后顺着横向速度再滑一段，ICE_K=0.12，最多 24；p.ax 做滑动动画）、**吊钩忽快忽慢**（L.pulse，G.hookRate）、**巨型捏捏**（L.giant，每 5 只来一只 1.4 倍的，压得整座塔一颤，更稳，+5 金币）。文案键 ch4 / ch5 / r_ice / r_pulse / r_giant。
- 机器人通过率（sk=0.06，每关 16 局）：第 4 章 44%–100%（最低第 38 关 44%、第 40 关 50%），第 5 章 75%–100%。第 5 章对机器人偏容易（它不受忽快忽慢影响），真人难度待试。
- 表单文字已改成 50 关 5 个世界。

## v6.3 试验版（11-21）：按住捏紧、松手落下
- 起因：用户问「核心玩法好玩吗、是不是太简单」。判断是核心只有「什么时候按」一个决定，每一下都一样；先做一个改操作本身的试验版让用户玩了再定。
- 玩法：按住（鼠标/触屏/空格）= 捏紧，吊钩上的捏捏被压扁、外面一圈进度环，0.75 秒捏满（SQ_FULL）；松手落下。捏得越满落得越快越重：塔的晃动增量 ×(1-0.65×蓄力)，捏满 +2 金币，捏满且完美再 +3 并且晃动 ×0.6。捏超过 1.7 秒（SQ_SLIP）会自己滑脱，按 0 蓄力掉下去。轻点一下 = 原来的普通落下。
- 代码：sqStart / sqEnd / sqTick，drop(charge)，p.charge，G.sq。`?sq=0` 可切回旧的一键操作做对比。文案键 tipSq / sqz。机器人不捏（蓄力 0），所以模拟的通过率和以前一样。
- **待用户试玩后决定**：留、调、还是去掉。

## 下一步
1. 用 `art/characters/` 里的 3 张图 → 裁边、压成 WebP 内嵌进 index.html（保持单文件、不发外部请求）；没有图的角色用原来的代码画法兜底。
2. 加压扁回弹等「捏」手感 → push 到本仓库 → 给用户 Pages 链接（加 `?v=N` 避缓存）在电脑和手机上看。
3. 用户满意 → 画剩下 31 只 → 背景、盲盒 → 第 3–7 条 → 做 CG 版投 CrazyGames。

## 代码说明
- 单个 index.html，Canvas 2D，约 170KB，音效 WebAudio 合成。11 语言（en fr it de es tr zh ja ko pt ru），文案在 TXT 对象，改文案 11 种一起改。
- SPECIES 数组：每只的 id、系列（pals/cafe/dream）、稀有度 r、颜色、shape、w/h（碰撞框，换图按这个比例）、trait（heavy/sticky/fluffy/wide/bouncy/gold）。
- 关卡 LV 数组（30 关 3 章）：n 目标层数、perf 三星完美数、wind、fast、narrow、drops、hearts。
- 数值：land()、update()、swingPeriod()/swingAmp()、CARDS、BOX_COST。
- 存档 localStorage 前缀 `sqs_`（owned、stars、shiny、coins、best、lvp、inv、bases、tutDone、dly、miss…）。
- 测试钩子（只在测试版）：`?auto=1&sk=0.06` 机器人自动玩；`window.__sq`（step、startRun、openStart、goStart、openMap、openShop、openBox、openColl、openLb、openDaily、openMiss、goTitle、LEVELS、setTut、setBest、revive、finishRun）。`/*TEST*/…/*ENDTEST*/` 之间的代码在平台版里会被去掉。
- 测试方法：Playwright 截图（多分辨率 640×360、960×540、1280×720、360×740、414×896，11 种语言不溢出）；假 SDK 检查调用顺序。

## 其他游戏
用户的总交接（所有游戏、账号、规则）在 claude.ai 项目文档「总交接-给ClaudeCode.md」，需要时找用户要。
