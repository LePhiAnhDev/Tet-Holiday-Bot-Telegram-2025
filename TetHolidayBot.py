import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, CallbackContext

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.full_name
    chat_id = update.message.chat.id

    welcome_message = (
        f"🧧 𝐂𝐇𝐔𝐂 𝐌𝐔𝐍𝐆 𝐍𝐀𝐌 𝐌𝐎𝐈 𝐓𝐄𝐓 𝐀𝐓 𝐓𝐘 𝟐𝟎𝟐𝟓 🧧\n"
        f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        f"💮 Chào mừng {user_name} 【🆔 {chat_id}】 đến với bot tết 2025.\n\n"
        f"🎇 Sản phẩm cung cấp các câu chúc tết chất lượng theo thông tin cụ thể được nhập từ người dùng.\n\n"
        f"🀄 Có trò chơi phong tục của Việt Nam thường được chơi vào ngày Tết.\n\n"
        f"📅 Đồng thời xem nhanh các thông tin về ngày âm lịch. 🇻🇳\n"
        f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        f"♨️ Vui lòng chọn chức năng ▾"
    )

    keyboard = [
        [InlineKeyboardButton("🎉 Chúc tết theo yêu cầu", callback_data="btn1"), InlineKeyboardButton("🌸 Câu thơ chúc tết", callback_data="btn2")],
        [InlineKeyboardButton("🍊 Câu chúc tết chung", callback_data="btn3"), InlineKeyboardButton("🔮 Gieo quẻ đầu năm", callback_data="btn5")],
        [InlineKeyboardButton("🌟 Tra cứu mệnh ngày - Giờ hoàng đạo - Tuổi xung", callback_data="btn4")],
        [InlineKeyboardButton("👨🏼‍💻 Giới thiệu về tôi", callback_data="btn6")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Dữ liệu tra cứu theo ngày
ngay_tra_cuu = {
    "ngay_1": "Mệnh ngày: Bình địa mộc\nGiờ hoàng đạo: Dần (3h-5h), Thìn (7h-9h), Tỵ (9h-11h), Thân (15h-17h), Dậu (17h-19h), Hợi (21h-23h)\nTuổi xung: Canh thìn, Bính thìn",
    "ngay_2": "Mệnh ngày: Bình địa mộc - Ngày hắc đạo\nGiờ hoàng đạo: Sửu (1h-3h), Thìn (7h-9h), Ngọ (11h-13h), Mùi (13h-15h), Tuất (19h-21h), Hợi (21h-23h)\nTuổi xung: Tân tị, Đinh tị.",
    "ngay_3": "Mệnh ngày: Bích thượng thổ - Ngày hoàng đạo\nGiờ hoàng đạo: Tý (23h-1h), Sửu (1h-3h), Mão (5h-7h), Ngọ (11h-13h), Thân (15h-17h), Dậu (17h-19h)\nTuổi xung: Nhâm ngọ, Bính ngọ, Giáp thân, Giáp dần",
    "ngay_4": "Mệnh ngày: Bích thượng thổ - Ngày hoàng đạo\nGiờ hoàng đạo: Dần (3h-5h), Mão (5h-7h), Tỵ (9h-11h), Thân (15h-17h), Tuất (19h-21h), Hợi (21h-23h)\nTuổi xung: Quý mùi, Đinh mùi, Ất dậu, Ất mão",
    "ngay_5": "Mệnh ngày: Kim bạc kim\nGiờ hoàng đạo: Tý (23h-1h), Sửu (1h-3h), Thìn (7h-9h), Tỵ (9h-11h), Mùi (13h-15h), Tuất (19h-21h)\nTuổi xung: Canh thân, Bính thân, Bính dần",
    "ngay_6": "Mệnh ngày: Kim bạc kim - Ngày hắc đạo\nGiờ hoàng đạo: Tý (23h-1h), Dần (3h-5h), Mão (5h-7h), Ngọ (11h-13h), Mùi (13h-15h), Dậu (17h-19h)\nTuổi xung: Tân dậu, Đinh dậu, Đinh mão",
    "ngay_7": "Mệnh ngày: Phú đăng hỏa\nGiờ hoàng đạo: Dần (3h-5h), Thìn (7h-9h), Tỵ (9h-11h), Thân (15h-17h), Dậu (17h-19h), Hợi (21h-23h)\nTuổi xung: Nhâm tuất, Canh tuất, Canh thìn",
    "ngay_8": "Mệnh ngày: Phú đăng hỏa - Ngày hoàng đạo\nGiờ hoàng đạo: Sửu (1h-3h), Thìn (7h-9h), Ngọ (11h-13h), Mùi (13h-15h), Tuất (19h-21h), Hợi (21h-23h)\nTuổi xung: Quý hợi, Tân hợi, Tân tị",
    "ngay_9": "Mệnh ngày: Thiên hà thủy - Ngày hắc đạo\nGiờ hoàng đạo: Tý (23h-1h), Sửu (1h-3h), Mão (5h-7h), Ngọ (11h-13h), Thân (15h-17h), Dậu (17h-19h)\nTuổi xung: Mậu tý, Canh tý",
    "ngay_10": "Mệnh ngày: Thiên hà thủy - Ngày hoàng đạo\nGiờ hoàng đạo: Dần (3h-5h), Mão (5h-7h), Tỵ (9h-11h), Thân (15h-17h), Tuất (19h-21h), Hợi (21h-23h)\nTuổi xung: Kỷ sửu, Tân sửu"
}

# Hàm xử lý khi người dùng bấm các button
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Xử lý chúc tết theo yêu cầu (btn1)
    if query.data == "btn1":
        keyboard = [
            [InlineKeyboardButton("Chúc ông bà", callback_data="chuc_ong_ba"), 
             InlineKeyboardButton("Chúc ba mẹ", callback_data="chuc_ba_me")],
            [InlineKeyboardButton("Chúc vợ chồng", callback_data="chuc_vo_chong"), 
             InlineKeyboardButton("Chúc anh em", callback_data="chuc_anh_em")],
            [InlineKeyboardButton("Chúc bạn bè", callback_data="chuc_ban_be"), 
             InlineKeyboardButton("Chúc người yêu / crush", callback_data="chuc_crush")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Vui lòng chọn người bạn muốn chúc Tết:", reply_markup=reply_markup)
        return

    # Xử lý các lựa chọn chúc tết theo yêu cầu
    if query.data in ["chuc_ong_ba", "chuc_ba_me", "chuc_vo_chong", "chuc_anh_em", "chuc_ban_be", "chuc_crush"]:
        context.user_data["chuc_doi_tuong"] = query.data
        await query.edit_message_text(f"Bạn đã chọn: {query.data.replace('_', ' ').title()}\nVui lòng nhập tên người được chúc:")
        return

    # Xử lý câu thơ chúc tết (btn2)
    if query.data == "btn2":
        poems = [
            "Năm mới chúc nhau sức khỏe, \nGia đình hạnh phúc vui vẻ quanh năm. \nLộc đến tài vô trăm lần, \nCông danh sự nghiệp muôn phần thăng hoa. 🚀",
            "Tân xuân chúc bạn phát tài, \nTiền vào như nước sông dài biển sâu. \nGia đình hạnh phúc bền lâu, \nCông danh sự nghiệp đứng đầu vinh quang. 🏆",
            "Xuân về rộn rã niềm vui, \nMuôn hoa đua nở ngát trời sắc xuân. \nChúc cho gia đạo an khang, \nPhúc đầy, lộc thịnh, ngập tràn yêu thương. 💖",
            "Xuân sang cánh én đưa thoi, \nTình xuân lan tỏa muôn nơi rạng ngời. \nChúc năm mới mãi rạng ngời, \nGia đình sum họp, trọn đời bình an. 🏡❤️",
            "Năm mới kính chúc mọi nhà, \nNiềm vui trọn vẹn, chan hòa yêu thương. \nCông danh phơi phới bốn phương, \nTài lộc phú quý, song đường hân hoan. 💰💖",
            "Xuân sang rộn rã tiếng cười, \nNhà nhà hạnh phúc, người người ấm êm. \nLộc vàng, tài lộc bên thềm, \nCông danh sự nghiệp ngày thêm rạng ngời. 🏆",
            "Năm mới chúc bạn an vui, \nGia đình hòa thuận, rạng ngời yêu thương. \nCông danh sự nghiệp rộng đường, \nPhúc lộc đầy ắp, vạn đường hanh thông. 💰",
            "Xuân về pháo nổ vang trời, \nChúc cho năm mới rạng ngời niềm vui. \nTiền vô như nước khắp nơi, \nGia đình sung túc, đời tươi thắm hồng. 🏡❤️",
            "Chúc cho năm mới thật vui, \nTài lộc phơi phới, nụ cười thênh thang. \nTình duyên rực rỡ, huy hoàng, \nGia đình đầm ấm, an khang suốt đời. 🏡🔥",
            "Xuân về rực rỡ muôn hoa, \nChúc cho năm mới nhà nhà bình yên. \nCông danh rạng rỡ vững bền, \nGia đình hạnh phúc, ấm êm sum vầy. ❤️🎉"
        ]
        for poem in poems:
            await query.message.reply_text(poem)
        await query.message.reply_text("Hãy nhập lệnh /start để quay trở lại trang chủ.")
        return

    # Xử lý chúc tết chung (btn3)
    if query.data == "btn3":
        keyboard = [
            [
                InlineKeyboardButton("Chúc Tết gia đình", callback_data="chuc_gia_dinh"),
                InlineKeyboardButton("Chúc Tết bạn bè", callback_data="chuc_ban_be_chung")
            ],
            [
                InlineKeyboardButton("Chúc Tết đồng nghiệp", callback_data="chuc_dong_nghiep"),
                InlineKeyboardButton("Chúc Tết khách hàng", callback_data="chuc_khach_hang")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Vui lòng chọn đối tượng chúc Tết chung:", reply_markup=reply_markup)
        return

    # Xử lý các lựa chọn chúc tết chung
    if query.data in ["chuc_gia_dinh", "chuc_ban_be_chung", "chuc_dong_nghiep", "chuc_khach_hang"]:
        messages = {
            "chuc_gia_dinh": [
                "Năm mới con xin chúc ba mẹ luôn khỏe mạnh, bình an, vui vẻ mỗi ngày. Mong ba mẹ sẽ luôn là chỗ dựa vững chắc cho con, là nguồn động viên, yêu thương bất tận. Chúc gia đình mình năm mới luôn ngập tràn tiếng cười, an khang thịnh vượng và mọi ước mơ đều thành hiện thực! 🌟👨‍👩‍👧‍👦❤️",
                "Tết đến, con xin kính chúc ông bà luôn sống vui, sống khỏe, sức khỏe dồi dào, sống lâu trăm tuổi. Chúc ba mẹ luôn hạnh phúc, công việc thuận lợi, gia đình mình luôn hòa thuận, ấm áp và tràn đầy tình thương yêu trong năm mới này. 🧧🍊🎋"
            ],
            "chuc_ban_be_chung": [
                "Năm mới chúc bạn luôn tươi vui, khỏe mạnh và luôn đạt được những ước mơ, hoài bão trong cuộc sống. Hy vọng trong năm nay chúng ta sẽ có thêm nhiều kỷ niệm đẹp, những chuyến đi vui vẻ và những trải nghiệm tuyệt vời. Chúc bạn một năm tràn ngập niềm vui, may mắn và thành công! 🥳✨🌻",
                "Năm mới lại về, chúc bạn một năm mới tràn đầy niềm vui, gặp nhiều may mắn trong công việc và cuộc sống. Mong rằng tình bạn của chúng ta sẽ ngày càng khăng khít hơn, cùng nhau tạo ra những kỷ niệm khó quên trong năm tới. 🕺🌸🌟"
            ],
            "chuc_dong_nghiep": [
                "Năm mới đến rồi, chúc anh/chị luôn giữ được tinh thần nhiệt huyết trong công việc, sức khỏe dồi dào để vượt qua mọi thử thách. Hy vọng trong năm nay, cả công ty chúng ta sẽ đạt được nhiều thành công, tiếp tục hợp tác, gắn bó và phát triển hơn nữa. 📈🌟🎉",
                "Năm mới chúc bạn sức khỏe dồi dào, công việc thuận lợi, gia đình hạnh phúc. Hy vọng chúng ta sẽ cùng nhau vượt qua những thử thách, đưa công ty chúng ta lên một tầm cao mới và gặt hái được những thành tựu rực rỡ. 🤝🌸📊"
            ],
            "chuc_khach_hang": [
                "Chúc Quý khách một năm mới an khang thịnh vượng, gia đình hạnh phúc, vạn sự như ý. Cảm ơn Quý khách đã đồng hành và tin tưởng chúng tôi trong suốt thời gian qua. Hy vọng trong năm mới này, chúng tôi sẽ tiếp tục được phục vụ Quý khách và mang lại những sản phẩm, dịch vụ tốt nhất. 🧧🎊🌟",
                "Nhân dịp năm mới, chúng tôi xin gửi đến Quý khách hàng lời chúc mừng năm mới an lành, hạnh phúc và thành công. Cảm ơn Quý khách đã tin tưởng và ủng hộ chúng tôi trong suốt thời gian qua. Mong rằng chúng tôi sẽ tiếp tục được phục vụ Quý khách và mang lại nhiều giá trị hơn nữa trong năm tới. 🎉🧧🎇"
            ]
        }
        for msg in messages.get(query.data, []):
            await query.message.reply_text(msg)
        await query.message.reply_text("Hãy nhập lệnh /start để quay trở lại trang chủ.")
        return

    # Xử lý gieo quẻ đầu năm (btn5)
    if query.data == "btn5":
        keyboard = [[InlineKeyboardButton(str(i), callback_data=f"quẻ_{i}") for i in range(j, min(j+4, 33))] for j in range(1, 33, 4)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Vui lòng chọn một quẻ (Để linh thiêng hãy chỉ chọn một quẻ):", reply_markup=reply_markup)
        return

    # Xử lý kết quả gieo quẻ
    if query.data.startswith("quẻ_"):
        gieo_que_messages = {
            f"quẻ_{i}": msg for i, msg in enumerate([
                "Gieo một quẻ là mở ra tương lai, chúc bạn đón nhận điều lành và thuận lợi!",
                "Thiên thời, địa lợi, nhân hòa – quẻ tốt đưa lối, vạn sự hanh thông!",
                "Gieo quẻ hôm nay, nhận lộc mai sau – chúc bạn phước duyên viên mãn!",
                "Mỗi quẻ gieo là một bài học, chúc bạn tìm ra hướng đi sáng suốt!",
                "Thiên cơ chỉ lộ cho người có duyên, chúc bạn hữu duyên với quẻ lành!",
                "Quẻ tốt hay xấu đều là chỉ dẫn, chúc bạn vững tâm để đi đúng đường!",
                "Gieo một quẻ an nhiên, đón một đời bình yên!",
                "Chúc bạn gieo quẻ gặp điềm lành, khai mở con đường hanh thông!",
                "Phong thủy hanh thông, tài lộc đầy nhà, công danh rộng mở!",
                "Chúc bạn đón vận may, tài lộc sum vầy, sự nghiệp vững bền!",
                "Quẻ tốt dẫn đường, vận hanh thông, phú quý cát tường!",
                "Thiên địa giao hòa, tiền vào như nước, vận đỏ như son!",
                "Cung tài bừng sáng, vận khí khai hoa, chúc bạn phát đạt muôn phần!",
                "Mệnh hợp phong thủy, phúc lộc vẹn toàn, giàu sang phú quý!",
                "Phong thủy đắc địa, nhà cửa vững bền, gia đạo an vui!",
                "Quẻ lành soi lối, tài lộc tràn đầy, vạn sự bình an!",
                "Chúc bạn vạn sự bình an, thân tâm an lạc, sức khỏe dồi dào!",
                "Phong thủy hòa hợp, tâm hồn thư thái, sức khỏe tràn đầy!",
                "Gieo quẻ an khang, đón nhận bình yên, một đời viên mãn!",
                "Thiên địa che chở, bình an bên bạn, sức khỏe vững bền!",
                "Nhà hợp phong thủy, thân hợp đất trời, an nhiên tự tại!",
                "Chúc bạn thân khỏe, tâm an, vận khí hanh thông như ý!",
                "Sống thuận tự nhiên, khỏe mạnh bình yên, đời an vui mãi!",
                "Phước lành che chở, sức khỏe tràn đầy, lòng không ưu lo!",
                "Gieo quẻ duyên lành, tình yêu viên mãn, hạnh phúc ngập tràn!",
                "Chúc bạn gặp đúng duyên, đúng người, đúng thời điểm!",
                "Nhân duyên tiền định, tình duyên bền lâu, trăm năm hạnh phúc!",
                "Quẻ tình duyên đẹp như ý, đôi lứa viên mãn trọn đời!",
                "Gia đạo bình an, tình duyên hòa hợp, vạn sự như ý!",
                "Tình duyên như quẻ son, trăm năm gắn bó vẹn toàn!",
                "Phong thủy hòa hợp, nhân duyên thăng hoa, gia đình hạnh phúc!",
                "Thiên định duyên lành, chúc bạn hạnh phúc trọn đời bên người thương!"
            ], start=1)
        }
        if query.data in gieo_que_messages:
            await query.message.reply_text(gieo_que_messages[query.data])
            await query.message.reply_text("Hãy nhập lệnh /start để quay trở lại trang chủ.")
        return

    # Xử lý tra cứu mệnh ngày (btn4)
    if query.data == "btn4":
        keyboard = [
            [InlineKeyboardButton("1 Tháng 1 năm Ất Tị nhuận, Tết Nguyên Đán", callback_data="ngay_1")],
            [InlineKeyboardButton("2 Tháng 1 năm Ất Tị nhuận, Tết Nguyên Đán", callback_data="ngay_2")],
            [InlineKeyboardButton("3 Tháng 1 năm Ất Tị nhuận, Tết Nguyên Đán", callback_data="ngay_3")],
            [InlineKeyboardButton("(4/1) Ngày Tân Sửu - Tháng Mậu Dần, năm Ất Tị nhuận", callback_data="ngay_4")],
            [InlineKeyboardButton("(5/1) Ngày Nhâm Dần - Tháng Mậu Dần, năm Ất Tị nhuận", callback_data="ngay_5")],
            [InlineKeyboardButton("(6/1) Ngày Quý Mão - Tháng Mậu Dần, năm Ất Tị nhuận", callback_data="ngay_6")],
            [InlineKeyboardButton("(7/1) Ngày Giáp Thìn - Tháng Mậu Dần, năm Ất Tị nhuận", callback_data="ngay_7")],
            [InlineKeyboardButton("(8/1) Ngày Ất Tỵ - Tháng Mậu Dần, năm Ất Tị nhuận", callback_data="ngay_8")],
            [InlineKeyboardButton("(9/1) Ngày Bính Ngọ - Tháng Mậu Dần, năm Ất Tị nhuận", callback_data="ngay_9")],
            [InlineKeyboardButton("(10/1) Ngày Đinh Mùi - Tháng Mậu Dần, năm Ất Tị nhuận", callback_data="ngay_10")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Vui lòng chọn một ngày để tra cứu:", reply_markup=reply_markup)
        return

    # Xử lý kết quả tra cứu ngày
    if query.data.startswith("ngay_"):
        if query.data in ngay_tra_cuu:
            await query.message.reply_text(ngay_tra_cuu[query.data])
            await query.message.reply_text("Hãy nhập lệnh /start để quay trở lại trang chủ.")
        return
    
     # Xử lý giới thiệu về tôi (btn6)
    if query.data == "btn6":
        about_me = (
            "👨‍💻 BACKEND DEVELOPER | LÊ PHI ANH\n\n"
            "🌟 DONATE ME:\n"
            "💳 1039506134 | LE PHI ANH\n"
            "Vietcombank - Ngân hàng Ngoại Thương Việt Nam\n\n"
            "🏦 MoMo | 0971390849\n"
            "LE PHI ANH\n\n"
            "📩 FOR WORK:\n"
            "- Discord: LePhiAnhDev\n"
            "- Telegram: @lephianh386ht\n"
            "- GitHub: https://github.com/LePhiAnhDev"
        )
        await query.message.reply_text(about_me)
        await query.message.reply_text("Hãy nhập lệnh /start để quay trở lại trang chủ.")
        return

# Hàm xử lý khi người dùng nhập tên
async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name_input = update.message.text
    chuc_doi_tuong = context.user_data.get("chuc_doi_tuong", "")

    if chuc_doi_tuong:
        await update.message.reply_text(f"Bạn đã nhập tên: {user_name_input}")
        
        chuc_mung = {
            "chuc_ong_ba": [
                "🎉 Chúc ông bà 🎉",
                f"Năm mới 2025, chúc {user_name_input} thật nhiều sức khỏe, sống lâu trăm tuổi và luôn vui vẻ bên con cháu! 🎉🌟",
                f"Chúc {user_name_input} năm mới bình an, khỏe mạnh và luôn là chỗ dựa vững chắc cho cả gia đình. 🏡❤️",
                f"Năm mới 2025, chúc {user_name_input} luôn tràn đầy niềm vui, sức khỏe dồi dào và niềm hạnh phúc vô tận. Mong rằng mỗi ngày trôi qua đều là một niềm vui mới, và ông bà sẽ mãi là ngọn đèn sáng dẫn lối cho gia đình ta. 🌟💖",
                f"Chúc {user_name_input} một năm mới an khang thịnh vượng, mãi mãi tươi trẻ, là nguồn động viên lớn lao cho con cháu. Hy vọng rằng những ngày Tết này sẽ tràn ngập niềm vui, tiếng cười và những kỷ niệm ấm áp bên nhau. 🌺🏡",
                f"Năm mới 2025, chúc {user_name_input} không chỉ có sức khỏe bền bỉ, mà còn tìm thấy niềm vui trong mỗi khoảnh khắc. Mong rằng ông bà sẽ cùng chúng con chia sẻ nhiều niềm vui, yêu thương và tiếng cười trong những dịp đoàn tụ. 🌸🎊",
                f"Hãy nhập lệnh /start để quay trở lại trang chủ.",
            ],
            "chuc_ba_me": [
                "🎊 Chúc cha mẹ 🎊",
                f"Tết Dương lịch 2025, chúc {user_name_input} thật nhiều sức khỏe, mọi việc suôn sẻ và hạnh phúc ngập tràn! 🎊🌺",
                f"Chúc năm mới {user_name_input} lúc nào cũng vui khỏe, mọi điều như ý, và mãi là tổ ấm yêu thương của cả nhà! 💖🎍",
                f"Tết Dương lịch 2025, chúc {user_name_input} không chỉ có thật nhiều sức khỏe, mà còn luôn tràn đầy niềm vui và hạnh phúc. Mong rằng mọi việc trong năm mới sẽ luôn suôn sẻ, và gia đình ta sẽ có nhiều kỷ niệm đẹp bên nhau. 🎊🌺",
                f"Chúc năm mới {user_name_input} luôn vui khỏe và hạnh phúc, mọi điều như ý muốn. Hy vọng tổ ấm của gia đình mình mãi mãi đong đầy tình yêu thương, tiếng cười và niềm vui mỗi ngày. 💖🎍",
                f"Tết Dương lịch 2025, chúc {user_name_input} luôn gặp may mắn và thành công trong mọi việc. Mong rằng cuộc sống của cha mẹ sẽ luôn ngập tràn niềm vui, hạnh phúc và những khoảnh khắc ấm áp bên gia đình. 🎉🌿",
                f"Hãy nhập lệnh /start để quay trở lại trang chủ.",
                
            ],
            "chuc_vo_chong": [
                "💑 Chúc vợ chồng 💑",
                f"Chúc {user_name_input} năm mới 2025 luôn xinh đẹp, hạnh phúc, và mãi là người vợ tuyệt vời nhất trong cuộc đời anh! 💕🌹✨",
                f"Tết đến, anh chúc {user_name_input} sức khỏe dồi dào, luôn yêu đời và mỗi ngày đều tràn ngập niềm vui bên anh! 🌸❤️",
                f"Chúc {user_name_input} năm mới 2025 luôn mạnh khỏe, thành công, và chúng ta sẽ cùng nhau vượt qua mọi thử thách để có một năm trọn vẹn! 🌟🤝",
                f"Tết Dương lịch đến, em chúc {user_name_input} mãi là người chồng yêu thương, luôn đồng hành cùng em trong mọi hành trình cuộc sống! 💑🌼",
                f"Năm mới 2025, chúc {user_name_input} luôn là nguồn động lực và niềm tự hào của anh/em. Mong rằng chúng ta sẽ cùng nhau trải qua thêm nhiều năm nữa đầy niềm vui, hạnh phúc và thành công. 🌟💖",
                f"Hãy nhập lệnh /start để quay trở lại trang chủ.",
            ],
            "chuc_anh_em": [
                "👨‍👩‍👦 Chúc anh em 👨‍👩‍👦",
                f"Chúc {user_name_input} năm mới 2025 thành công rực rỡ, sức khỏe dồi dào và luôn gặp nhiều may mắn! 🎆💪",
                f"Năm mới đến, chúc {user_name_input} mọi điều tốt lành, hạnh phúc viên mãn và ngày càng thăng tiến trong cuộc sống! 🌟🚀",
                f"Tết Dương lịch 2025, chúc {user_name_input} luôn mạnh mẽ, kiên cường và thành công trong mọi hành trình. Hy vọng rằng năm mới sẽ mang đến nhiều cơ hội và niềm vui. 🌠💪",
                f"Chúc {user_name_input} năm mới an lành, tràn đầy niềm vui và đạt được những ước mơ mà bạn luôn ấp ủ. Chúc cho mọi bước đi của bạn đều dẫn đến thành công và hạnh phúc. 🌈🏆",
                f"Tết Dương lịch 2025, chúc {user_name_input} đạt được nhiều thành công trong công việc, cuộc sống hạnh phúc và sức khỏe dồi dào. Mong rằng tình anh em của chúng ta sẽ ngày càng bền chặt và gắn bó hơn nữa. 🎆💪",
                f"Hãy nhập lệnh /start để quay trở lại trang chủ.",
            ],
            "chuc_ban_be": [
                "🎉 Chúc bạn bè 🎉",
                f"Chúc {user_name_input} năm mới 2025 thật nhiều sức khỏe, niềm vui tràn ngập, và thành công như ý! 🎊✨",
                f"Tết Dương lịch 2025, chúc {user_name_input} luôn hạnh phúc, gặp nhiều may mắn và đạt được mọi ước mơ! 🌈🏆",
                f"Năm mới đến rồi, chúc {user_name_input} lúc nào cũng vui vẻ, công việc thuận lợi và tình yêu trọn vẹn! 💌🎁",
                f"Chúc {user_name_input} năm 2025 thật nhiều tài lộc, sức khỏe dồi dào và mãi giữ được sự lạc quan, yêu đời! 🤑🌟",
                f"Năm mới 2025, chúc tình bạn của chúng ta thêm bền chặt và bạn luôn đạt được những điều tốt đẹp nhất! 🤝💖",
                f"Hãy nhập lệnh /start để quay trở lại trang chủ.",
            ],
            "chuc_crush": [
                "💑 Chúc người yêu / crush 💑",
                f"Chúc {user_name_input} năm mới thật nhiều niềm vui, sức khỏe và luôn bên cạnh anh. Mong chúng ta sẽ có thật nhiều khoảnh khắc hạnh phúc trong năm 2025! 💑🎇",
                f"Năm mới, chúc {user_name_input} luôn tươi cười, hạnh phúc và đón nhận mọi điều tốt đẹp nhất. Anh sẽ luôn ở đây, cùng em bước qua mọi thăng trầm. 🌹✨",
                f"Chúc {user_name_input} một năm mới tràn ngập yêu thương và những điều tuyệt vời. Hy vọng năm nay chúng ta sẽ gần nhau hơn. 💖💫",
                f"Chúc {user_name_input} một năm mới vui vẻ, hạnh phúc, và 2025 sẽ là một năm tuyệt vời của chúng ta! 🎊💍",
                f"Năm mới, chúc {user_name_input} tất cả những điều tốt đẹp nhất, và hy vọng năm nay sẽ là năm mà chúng ta tạo ra thật nhiều kỷ niệm đáng nhớ. 🌸❤️",
                f"Hãy nhập lệnh /start để quay trở lại trang chủ.",
            ]
        }
        
        for msg in chuc_mung.get(chuc_doi_tuong, []):
            await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Hãy bắt đầu bằng cách chọn đối tượng chúc Tết trước.")

async def main():
    TOKEN = 'ENTER YOU BOT TOKEN'
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_input))
    
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())