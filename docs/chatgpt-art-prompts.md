# 捏捏叠叠乐 — ChatGPT 画图提示词

2026-11-16。用来把游戏里用代码画的 34 只捏捏换成正式美术，准备投 CrazyGames。

## 怎么画（顺序很重要）

1. **先定风格**：在一个新的 ChatGPT 对话里发「风格母版」+ 水豚那一行，反复调到满意。之后**所有角色都在同一个对话里画**，每次都说 "same style as the capybara"，风格才不会跑。（已完成：水豚、饺子、六角恐龙，见 HANDOFF.md）
2. **先只画 3 只**：水豚 capy、饺子 dump、六角恐龙 axo（开局就有的三只）。先接进游戏，看叠起来、晃起来的效果，没问题再画剩下的 31 只。
3. 每张图下载成 PNG，**文件名用下面表格里的 id**（比如 capy.png）。
4. 背景和盲盒在角色定稿之后再画。

## 统一要求（每张都要满足）

- **透明背景** PNG，1536×1024（横图）。
- **正面稍微从上往下看**，角色像软软的捏捏玩具（squishy toy），**底部和顶部要比较平**，这样叠起来看着稳。
- 角色**左右撑满画面约 90%**，上下居中，四周不要留阴影、地面、文字、边框。
- 脸画在身上：**简单的黑豆眼 + 小嘴 + 腮红**，表情开心平静。紧张时的冒汗、发抖用代码加。
- 宽高比尽量接近表格里的「宽:高」，太高或太瘦会被挤扁变形。

## 风格母版（每次画角色时放在最前面）

```
Cute kawaii squishy toy character for a casual mobile game. Soft, puffy, slightly glossy 3D-rendered look like a mochi squishy toy, gentle soft lighting from the top, subtle soft highlight, pastel saturated colors, thick rounded shapes, no outlines or very soft outline. Simple face: two small shiny black bead eyes, tiny smile, pink blush cheeks. Front view, slightly from above. The character's top and bottom are fairly flat so it can be stacked. Fills about 90% of the image width, centered. Transparent background, no shadow, no ground, no text. 1536x1024.
```

画后面的角色时，在前面加一句：`Same style, lighting, face and canvas as the capybara. Now draw:`

## 34 只角色

宽:高 是游戏里的碰撞框比例（SPECIES 的 w/h），照着画最好。

### 萌宠系列 Squishy Pals

| id | 中文 | 宽:高 | 稀有度 | 提示词（接在风格母版后面） |
|---|---|---|---|---|
| capy | 水豚 | 1.7:1 | 普通 | a chubby brown capybara (#c08a58) with a lighter tan belly, tiny round ears, blunt square snout, lying down like a loaf |
| axo | 六角恐龙 | 1.6:1 | 普通 | a pink axolotl (#ffb1c9) with a pale pink belly and three fluffy frilly gills on each side of the head, lying flat |
| cow | 高地牛 | 1.55:1 | 普通 | a fluffy ginger highland cow (#c8733c) with shaggy fringe over the eyes and two small curved horns, lying down |
| frog | 青蛙 | 1.75:1 | 普通 | a round green frog (#86cf68) with a pale green belly and two big bulging eyes on top, sitting flat |
| shiba | 柴犬 | 1.55:1 | 普通 | an orange shiba inu (#f2a65a) with a cream white face and belly, pointy ears, curled up like a loaf |
| rpanda | 小熊猫 | 1.55:1 | 普通 | a red panda (#c9572f) with a white face mask, round ears with white tips, curled up |
| shark | 鲨鱼 | 2.1:1 | 普通 | a long blue-grey baby shark (#7fa9cc) with a white belly and a small dorsal fin, lying sideways, wide and flat |
| peng | 企鹅 | 1.3:1 | 稀有 | a plump navy penguin (#3f4d6e) with a big white belly and a small orange beak, sitting |
| cat | 橘猫 | 1.5:1 | 稀有 | a cream-orange cat (#ffcf78) with a pale belly and pointy ears, curled up like a loaf |
| bear | 棕熊 | 1.5:1 | 稀有 | a brown teddy bear (#a7795b) with a tan belly and round ears, lying down |
| sloth | 树懒 | 1.6:1 | 稀有 | a beige sloth (#b6a28c) with dark eye patches and a cream face, hugging itself, sleepy smile |
| dino | 小恐龙 | 1.6:1 | 稀有 | a light green baby dinosaur (#8cd47e) with a pale belly and small soft spikes along its back, lying down |
| gcapy | 金水豚 | 1.7:1 | 超稀有 | the same capybara but made of shiny gold (#ffd23f), sparkles around it, glossy metallic but still soft and cute |

### 甜点系列 Sweet Café

| id | 中文 | 宽:高 | 稀有度 | 提示词 |
|---|---|---|---|---|
| dump | 饺子 | 1.8:1 | 普通 | a plump white steamed dumpling (#fbf3e4) with pleated folds on top, lying flat |
| cro | 可颂 | 2.45:1 | 普通 | a golden-brown croissant (#e8a64c) with layered crescent ridges, very wide and flat |
| mochi | 麻糬 | 1.6:1 | 普通 | a soft pink round mochi (#f8dcea) dusted with a little powder, flat bottom |
| bun | 包子 | 1.6:1 | 普通 | a white fluffy steamed bun (#fff4e2) with a swirl on top, flat bottom |
| oni | 饭团 | 1.5:1 | 普通 | a triangle rice ball onigiri (#ffffff) with a nori seaweed strip at the bottom, face on the rice above the nori |
| sushi | 寿司 | 1.95:1 | 普通 | a salmon nigiri sushi: white rice base (#fffaf2) with an orange salmon slice on top, face on the rice |
| toast | 吐司 | 1.65:1 | 稀有 | a thick slice of toast (#f3cf8f) with golden crust edges and a pat of butter on top |
| boba | 珍珠奶茶 | 1.2:1 | 稀有 | a short chubby bubble tea cup (#f1d6b8) with dark tapioca pearls at the bottom, a dome lid and straw, face on the cup |
| donut | 甜甜圈 | 1.95:1 | 稀有 | a donut (#e7b073) with pink frosting (#ff9cc6) and colorful sprinkles, seen from the side so it looks wide and flat |
| pud | 布丁 | 1.55:1 | 稀有 | a wobbly custard pudding (#ffd66b) with dark caramel on top, flat bottom |
| berry | 草莓 | 1.45:1 | 稀有 | a plump red strawberry (#ff5c6c) with seeds and a green leaf crown on top, lying on its side |
| rdonut | 彩虹甜甜圈 | 1.95:1 | 超稀有 | the same donut but with shimmering rainbow frosting and sparkles, glossy |

### 梦幻夜系列 Dreamy Night

| id | 中文 | 宽:高 | 稀有度 | 提示词 |
|---|---|---|---|---|
| jelly | 果冻 | 1.6:1 | 普通 | a translucent light-blue jelly blob (#7fd8ff), see-through with soft inner glow, flat bottom |
| ghost | 小幽灵 | 1.4:1 | 普通 | a soft white little ghost (#f7f4ff) with a wavy bottom edge, floating low, flat-ish bottom |
| cloud | 云朵 | 2.25:1 | 普通 | a fluffy white cloud (#ffffff) with puffy bumps on top, wide and flat bottom |
| mush | 蘑菇 | 1.5:1 | 普通 | a mushroom with a big red cap (#ff6b6b) with white spots and a short cream stem, face on the stem |
| bat | 蝙蝠 | 1.55:1 | 普通 | a round purple baby bat (#6d5a8c) with a lighter belly and small folded wings, pointy ears |
| bunny | 兔子 | 1.55:1 | 稀有 | a lavender bunny (#dccdff) with long ears folded back flat, lying down |
| uni | 独角兽 | 1.55:1 | 稀有 | a white-pink unicorn (#fff5fb) with a small golden horn and a pastel rainbow mane, lying down |
| dragon | 小龙 | 1.55:1 | 稀有 | a mint baby dragon (#7fd6c2) with a pale belly, tiny horns and small wings, lying down |
| cosmo | 星空六角恐龙 | 1.6:1 | 超稀有 | the axolotl but with a deep purple galaxy body (#6c5ad8) full of tiny stars, glowing gills, sparkles |

## 背景（角色定稿后再画）

```
Background art for a cute casual mobile stacking game, same soft kawaii 3D style as the characters. Vertical tall image 1024x1536. Soft pastel colors, low detail in the middle so stacked characters stay readable, gentle gradient sky. No characters, no text.
```

后面分别接：

- 萌宠系列：`a sunny flower garden with soft rolling hills at the bottom and fluffy clouds in a pink-blue sky`
- 甜点系列：`a dreamy sweet bakery: cake and candy hills at the bottom, warm peach sky with floating sprinkles`
- 梦幻夜系列：`a night sky with a big soft moon, tiny stars and purple clouds at the bottom`

## 盲盒（3 个系列各一个）

```
A cute blind box toy package, same soft kawaii 3D style, front view, transparent background, 1024x1024, no text. A rounded box with a big question mark and a ribbon, color: ___
```

- 萌宠：pink (#ff9cc0)；甜点：peach orange (#ffcf8a)；梦幻夜：lavender purple (#a99cff)

## 接进游戏时要做的

- 图片去背景、裁边、压缩成 WebP、内嵌进单个 index.html（保持一个文件、不发外部请求）。
- 用代码做捏捏的压扁回弹、被压着微微变形、紧张时冒汗发抖；闪光版（shiny）用代码加色调和光效，不用另画。
- 图鉴、盲盒、商店里的小图都用同一套素材缩小。
