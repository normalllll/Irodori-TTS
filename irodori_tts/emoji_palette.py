"""The emoji the text accepts as speech direction, for interfaces to offer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EmojiPaletteItem:
    emoji: str
    label: str
    description: str


EMOJI_PALETTE_ITEMS: tuple[EmojiPaletteItem, ...] = (
    EmojiPaletteItem("👂", "囁き", "耳元の音"),
    EmojiPaletteItem("😮‍💨", "吐息", "溜息、寝息"),
    EmojiPaletteItem("⏸️", "間", "沈黙"),
    EmojiPaletteItem("🤭", "笑い", "くすくす、含み笑い"),
    EmojiPaletteItem("🥵", "喘ぎ", "うめき声、唸り声"),
    EmojiPaletteItem("📢", "エコー", "リバーブ"),
    EmojiPaletteItem("😏", "からかう", "甘えるように"),
    EmojiPaletteItem("🥺", "震え声", "自信なさげに"),
    EmojiPaletteItem("🌬️", "息切れ", "荒い息遣い、呼吸音"),
    EmojiPaletteItem("😮", "息をのむ", "Gasp"),
    EmojiPaletteItem("👅", "舐める音", "咀嚼音、水音"),
    EmojiPaletteItem("💋", "リップノイズ", "Lip smack"),
    EmojiPaletteItem("🫶", "優しく", "Tenderly"),
    EmojiPaletteItem("😭", "泣き声", "嗚咽、悲しみ"),
    EmojiPaletteItem("😱", "悲鳴", "叫び、絶叫"),
    EmojiPaletteItem("😪", "眠そう", "気だるげに"),
    EmojiPaletteItem("😴", "寝言", "いびき"),
    EmojiPaletteItem("⏩", "早口", "一気に、急いで"),
    EmojiPaletteItem("📞", "電話越し", "スピーカー越し"),
    EmojiPaletteItem("🐢", "ゆっくり", "Slowly"),
    EmojiPaletteItem("🥤", "飲み込む", "唾を飲む音"),
    EmojiPaletteItem("🤧", "咳・鼻", "咳き込み、鼻すすり"),
    EmojiPaletteItem("😒", "舌打ち", "Tutting"),
    EmojiPaletteItem("😰", "慌てる", "動揺、緊張、どもり"),
    EmojiPaletteItem("😆", "喜び", "嬉しそうに"),
    EmojiPaletteItem("💥", "勢いよく", "力強い勢い"),
    EmojiPaletteItem("😠", "怒り", "不満げ、拗ねる"),
    EmojiPaletteItem("😲", "驚き", "感嘆"),
    EmojiPaletteItem("🥱", "あくび", "Yawn"),
    EmojiPaletteItem("😖", "苦しげ", "Agonizingly"),
    EmojiPaletteItem("😟", "心配", "不安そうに"),
    EmojiPaletteItem("🫣", "照れ", "恥ずかしそうに"),
    EmojiPaletteItem("🙄", "呆れ", "Exasperatedly"),
    EmojiPaletteItem("😊", "楽しげ", "嬉しそうに"),
    EmojiPaletteItem("😎", "得意げ", "自信ありげに"),
    EmojiPaletteItem("👌", "相槌", "頷く音"),
    EmojiPaletteItem("🙏", "懇願", "お願いするように"),
    EmojiPaletteItem("🥴", "酔う", "Drunkenly"),
    EmojiPaletteItem("🎵", "鼻歌", "Humming"),
    EmojiPaletteItem("🤐", "口を塞ぐ", "Muffled"),
    EmojiPaletteItem("😌", "安堵", "満足げに"),
    EmojiPaletteItem("🤔", "疑問", "Questioning"),
    EmojiPaletteItem("💪", "力強く", "力を込めて"),
    EmojiPaletteItem("👃", "嗅ぐ音", "匂いを嗅ぐ音"),
    EmojiPaletteItem("📖", "朗読", "ナレーション"),
)
