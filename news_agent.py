import os
import datetime
import feedparser
from anthropic import Anthropic
from gtts import gTTS

OUTPUT_DIR = os.path.expanduser("~/News")
os.makedirs(OUTPUT_DIR, exist_ok=True)

client = Anthropic()  # يقرأ ANTHROPIC_API_KEY من متغيرات البيئة

# ضع مصادرك هنا: أخبار عالمية، أعمال، ومحلية
SOURCES = {
    "أخبار عالمية": ["https://feeds.bbci.co.uk/news/world/rss.xml"],
    "أخبار الأعمال": ["https://feeds.bbci.co.uk/news/business/rss.xml"],
    "أخبار محلية": ["https://example.com/your-local-feed.xml"],  # استبدله بمصدرك
}

# نبرة التقرير الصوتية: عدّلها كما تشاء
TONE = "مذيع أخبار محترف، هادئ وواضح، يبدأ بأهم خبر، ويختم بجملة ختامية قصيرة"


def fetch_items(urls, limit=6):
    items = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit]:
            items.append(f"- {entry.get('title', '')}: {entry.get('summary', '')[:300]}")
    return items


def write_report(sections):
    material = ""
    for name, urls in sections.items():
        items = fetch_items(urls)
        if items:
            material += f"\n## {name}\n" + "\n".join(items) + "\n"

    if not material.strip():
        raise RuntimeError("لم يتم جلب أي أخبار. تحقق من مصادر RSS والاتصال بالإنترنت.")

    prompt = f"""اكتب تقرير أخبار صباحي باللغة العربية الفصحى المبسطة، مناسب للقراءة الصوتية.
النبرة: {TONE}.
القواعد:
- قسّم التقرير حسب الأقسام الموجودة في المادة.
- لا تستخدم Markdown ولا قوائم ولا رموز، فالنص سيُحوَّل إلى صوت.
- اجعل الجمل قصيرة وواضحة، واذكر الأرقام بوضوح.
- لا تختلق أخبارًا غير موجودة في المادة.
- الطول: نحو 400 إلى 600 كلمة.

المادة الخام:
{material}"""

    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def text_to_speech(text, path):
    gTTS(text=text, lang="ar", slow=False).save(path)


def run():
    today = datetime.date.today().isoformat()
    report = write_report(SOURCES)

    txt_path = os.path.join(OUTPUT_DIR, f"report_{today}.txt")
    mp3_path = os.path.join(OUTPUT_DIR, f"report_{today}.mp3")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report)

    text_to_speech(report, mp3_path)
    print(f"تم إنشاء التقرير: {mp3_path}")


if __name__ == "__main__":
    run()
