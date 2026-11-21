# Squishy Stack · CrazyGames 提交材料

## 文件（都在仓库里）
| 表单项 | 文件 |
|---|---|
| 游戏包（HTML5，index.html 在 zip 根目录） | `dist/squishy-stack-crazygames.zip` |
| 封面 1920×1080 | `art/final/squishy-stack-cg-1920x1080.png`（**还没做**） |
| 封面 800×1200 | `art/final/squishy-stack-cg-800x1200.png`（**还没做**） |
| 封面 800×800 | `art/final/squishy-stack-cg-800x800.png`（**还没做**） |
| 预览视频 横 1920×1080（18 秒，无声） | `submission/preview-1920x1080.mp4` |
| 预览视频 竖 1080×1620（18 秒，无声） | `submission/preview-1080x1620.mp4` |

封面做好后重新跑一次 `node tools/make-video.js`，视频开头会自动加上 0.8 秒封面（CrazyGames 要求第一帧是封面）。

## 表单选项建议
- 引擎：HTML5（自己写的，纯 Canvas）。**Engine / Tools 不选任何 AI 相关选项**（用户规矩）。
- 如果表单单独问「是否使用了 AI 生成的内容」：由用户自己决定怎么填，会话不替用户选。
- 支持手机：是（竖屏和横屏都能玩，竖屏体验最好）。
- 存档：浏览器 localStorage，没有接 CG Data Module。
- 联机：否。
- 静音：支持 SDK（读 `settings.muteAudio`，并跟着改）。
- 语言：English, 中文, Français, Italiano, Deutsch, Español, Türkçe, 日本語, 한국어, Português, Русский（11 种，按平台语言自动选）。
- 分类：Casual（下拉里有 Arcade / Skill 也可以）。
- Tags（按下拉里实际有的选）：Stacking, One Button, Physics, Cute, Animal, Collecting, Casual, 2D, Mobile.
- 全屏：勾。

## Title
Squishy Stack

## Description
Squishy Stack is a one-button stacking game with soft, squishy toys. A swinging hook carries a squishy capybara, dumpling, axolotl or one of 30 other characters. Tap at the right moment to drop it onto the tower. Every landing squashes and bounces, the squishies below get pressed flat, and the whole tower leans and wobbles like jelly. Land dead centre for a Perfect, chain three Perfects to start Squishy Fever, and try not to let the tower topple.

Features:
- 30 levels in 3 worlds: a flower garden, a sweet bakery and a dreamy night sky
- New twists as you go: wind, birds, sky coins, a sliding base, bouncy clouds and flickering lights
- Endless mode with rivals to overtake
- 34 squishies to collect from blind boxes, each with its own trait, plus a toy room where you can poke them
- Squishy Fever, three-of-a-kind bonuses, power-ups, daily gifts and missions
- 11 languages

## Controls
Click, tap or press Space to drop the squishy · S shockwave (calms the wobble) · D blink (auto-centres the next drop) · 1 / 2 / 3 choose a power · P pause · M mute
