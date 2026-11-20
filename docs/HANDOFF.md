# 捏捏叠叠乐 Squishy Stack · 交接（给 Claude Code）

更新：2026-11-17。全程中文回复；用户不看代码，只看效果，说话直白。

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
