# وكيل تقارير الأخبار الصوتية

يجلب الأخبار من مصادر RSS، ويكتب تقريرًا باللغة العربية عبر Claude، ثم يحوّله إلى ملف صوتي (MP3) يُحفظ في مجلد `~/News`.

## التثبيت

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
```

## التشغيل اليدوي

```bash
python3 news_agent.py
```

## التشغيل اليومي

### macOS
1. انسخ `com.news.agent.plist` إلى `~/Library/LaunchAgents/`.
2. عدّل المسار في `ProgramArguments` ليشير إلى مكان `news_agent.py`.
3. ضع مفتاحك في `ANTHROPIC_API_KEY`.
4. فعّل المهمة:
```bash
launchctl load ~/Library/LaunchAgents/com.news.agent.plist
```

### Windows
استخدم "جدولة المهام" (Task Scheduler)، واختر تشغيل `python.exe` مع مسار `news_agent.py`، وفعّل خيار "Run task as soon as possible after a scheduled start is missed".

### Linux
استخدم systemd timer مع `Persistent=true`.

## تخصيص المصادر والنبرة

عدّل `SOURCES` لإضافة مصادر RSS، وعدّل `TONE` لتغيير أسلوب المذيع.

## أمان

لا تضع مفتاح API داخل الكود أو ترفعه إلى GitHub. ملف `.gitignore` يستثني ملف `plist` لأنه قد يحتوي على المفتاح.
