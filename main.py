import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Настройки
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
ADMIN_ID = 664576828 # <-- Ваш ID, куда будут приходить заявки

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Логика бота (обработка команд)
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем кнопку под сообщением
    kb = [
        [InlineKeyboardButton(
            text="🚀 ОСТАВИТЬ ЗАЯВКУ", 
            web_app=WebAppInfo(url=os.environ.get("WEBHOOK_URL")) # Ссылка подставится автоматически
        )]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    # Текст приветствия
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Мы разрабатываем современные Telegram Mini Apps для бизнеса.\n"
        "Нажмите на кнопку ниже, чтобы заполнить короткий бриф, и мы свяжемся с вами в течение 15 минут."
    )
    
    await message.answer(welcome_text, reply_markup=keyboard)
# Жизненный цикл FastAPI (Установка вебхука при старте)
@asynccontextmanager
async def lifespan(app: FastAPI):
    if WEBHOOK_URL:
        await bot.set_webhook(url=f"{WEBHOOK_URL}/webhook", drop_pending_updates=True)
    yield
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

# ВАШЕ HTML ПРИЛОЖЕНИЕ (Вставлено напрямую в Python)
# ВНИМАНИЕ: Используются обычные кавычки """, а не f""" , чтобы не сломался JavaScript внутри
html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Разработка мини приложений</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;700;900&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
  :root { --bg: #0a0d14; --bg-2: #11151f; --fg: #f5f7fa; --muted: #8a92a6; --accent: #ff5e3a; --accent-2: #00d9c0; --accent-3: #ffb800; --card: rgba(255,255,255,0.04); --border: rgba(255,255,255,0.08); }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  body { margin: 0; font-family: 'Manrope', sans-serif; background: var(--bg); color: var(--fg); min-height: 100vh; overflow-x: hidden; }
  .display-font { font-family: 'Unbounded', sans-serif; }
  .bg-mesh { position: fixed; inset: 0; z-index: -2; background: radial-gradient(ellipse 80% 50% at 20% 0%, rgba(255,94,58,0.18), transparent 60%), radial-gradient(ellipse 60% 50% at 80% 30%, rgba(0,217,192,0.14), transparent 60%), radial-gradient(ellipse 50% 50% at 50% 100%, rgba(255,184,0,0.10), transparent 60%), var(--bg); }
  .bg-grid { position: fixed; inset: 0; z-index: -1; background-image: linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px); background-size: 44px 44px; mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%); -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%); }
  .particle { position: fixed; width: 4px; height: 4px; border-radius: 50%; pointer-events: none; z-index: -1; animation: float-up linear infinite; }
  @keyframes float-up { 0% { transform: translateY(110vh) translateX(0) scale(1); opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { transform: translateY(-10vh) translateX(60px) scale(0.4); opacity: 0; } }
  .tg-icon-wrap { position: relative; width: 84px; height: 84px; margin: 0 auto 18px; }
  .tg-icon-wrap::before { content: ''; position: absolute; inset: -8px; background: linear-gradient(135deg, #2aabee, #229ed9); border-radius: 28px; filter: blur(24px); opacity: 0.6; animation: glow 3s ease-in-out infinite; }
  @keyframes glow { 0%,100% { opacity: 0.4; transform: scale(0.95); } 50% { opacity: 0.75; transform: scale(1.08); } }
  .tg-icon { position: relative; width: 84px; height: 84px; background: linear-gradient(135deg, #2aabee 0%, #229ed9 100%); border-radius: 24px; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 40px -10px rgba(42,171,238,0.5), inset 0 1px 0 rgba(255,255,255,0.3); animation: float 3.5s ease-in-out infinite; }
  @keyframes float { 0%,100% { transform: translateY(0) rotate(-4deg); } 50% { transform: translateY(-6px) rotate(4deg); } }
  .card { background: var(--card); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid var(--border); border-radius: 20px; }
  .section-label { display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px; background: rgba(255,94,58,0.12); border: 1px solid rgba(255,94,58,0.35); border-radius: 100px; color: var(--accent); font-size: 11px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; }
  .chip { display: inline-flex; align-items: center; padding: 10px 14px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); cursor: pointer; transition: all 0.2s; font-size: 13px; font-weight: 500; user-select: none; color: var(--fg); }
  .chip:hover { background: rgba(255,255,255,0.06); border-color: rgba(255,94,58,0.4); transform: translateY(-1px); }
  .chip.active { background: linear-gradient(135deg, rgba(255,94,58,0.18), rgba(255,184,0,0.08)); border-color: var(--accent); color: var(--accent); box-shadow: 0 4px 12px -2px rgba(255,94,58,0.3); }
  .style-card { position: relative; padding: 12px; border-radius: 14px; background: rgba(255,255,255,0.03); border: 2px solid var(--border); cursor: pointer; transition: all 0.25s; overflow: hidden; }
  .style-card:hover { border-color: rgba(0,217,192,0.4); transform: translateY(-2px); }
  .style-card.active { border-color: var(--accent-2); background: rgba(0,217,192,0.08); box-shadow: 0 6px 18px -4px rgba(0,217,192,0.25); }
  .style-preview { height: 56px; border-radius: 8px; margin-bottom: 8px; position: relative; overflow: hidden; }
  .style-preview::after { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 50%, rgba(0,0,0,0.15) 100%); }
  .palette { display: flex; height: 38px; border-radius: 10px; overflow: hidden; cursor: pointer; border: 2px solid transparent; transition: all 0.2s; flex: 1; }
  .palette:hover { transform: translateY(-1px); }
  .palette.active { border-color: var(--fg); transform: scale(1.03); box-shadow: 0 6px 18px -4px rgba(255,255,255,0.2); }
  .palette > div { flex: 1; transition: flex 0.3s; }
  .input { width: 100%; padding: 14px 16px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; color: var(--fg); font-family: inherit; font-size: 15px; transition: all 0.2s; }
  .input::placeholder { color: var(--muted); }
  .input:focus { outline: none; border-color: var(--accent); background: rgba(255,94,58,0.05); box-shadow: 0 0 0 3px rgba(255,94,58,0.15); }
  input[type="range"] { -webkit-appearance: none; appearance: none; width: 100%; height: 6px; background: linear-gradient(90deg, var(--accent) 0%, var(--accent) var(--val,10%), rgba(255,255,255,0.1) var(--val,10%)); border-radius: 3px; outline: none; }
  input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; width: 22px; height: 22px; background: var(--fg); border: 3px solid var(--accent); border-radius: 50%; cursor: pointer; box-shadow: 0 4px 10px -2px rgba(0,0,0,0.4); }
  .btn-submit { position: relative; background: linear-gradient(135deg, var(--accent) 0%, #ff8c5a 50%, var(--accent-3) 100%); background-size: 200% 100%; color: white; font-weight: 700; padding: 18px; border-radius: 16px; border: none; cursor: pointer; font-family: 'Unbounded', sans-serif; font-size: 15px; letter-spacing: 0.5px; transition: all 0.4s; overflow: hidden; box-shadow: 0 12px 30px -8px rgba(255,94,58,0.5); }
  .btn-submit:hover { background-position: 100% 0; transform: translateY(-2px); box-shadow: 0 18px 40px -8px rgba(255,94,58,0.6); }
  .btn-submit:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }
  .success-overlay { position: fixed; inset: 0; background: rgba(10,13,20,0.92); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); display: flex; align-items: center; justify-content: center; z-index: 100; opacity: 0; pointer-events: none; transition: opacity 0.4s; padding: 20px; }
  .success-overlay.show { opacity: 1; pointer-events: all; }
  .success-card { transform: scale(0.85) translateY(20px); transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }
  .success-overlay.show .success-card { transform: scale(1) translateY(0); }
  .checkmark-circle { width: 110px; height: 110px; border-radius: 50%; background: linear-gradient(135deg, var(--accent-2) 0%, #00f5d4 100%); display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; box-shadow: 0 0 60px rgba(0,217,192,0.5), inset 0 2px 0 rgba(255,255,255,0.3); animation: pulse-glow 2s ease-in-out infinite; position: relative; }
  .checkmark-circle::before { content: ''; position: absolute; inset: -8px; border: 2px solid rgba(0,217,192,0.3); border-radius: 50%; animation: ring-expand 2s ease-out infinite; }
  @keyframes ring-expand { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(1.5); opacity: 0; } }
  @keyframes pulse-glow { 0%,100% { box-shadow: 0 0 40px rgba(0,217,192,0.4), inset 0 2px 0 rgba(255,255,255,0.3); } 50% { box-shadow: 0 0 80px rgba(0,217,192,0.7), inset 0 2px 0 rgba(255,255,255,0.3); } }
  .checkmark-svg { width: 56px; height: 56px; stroke: white; stroke-width: 3.5; fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 60; stroke-dashoffset: 60; animation: draw-check 0.6s 0.3s forwards ease-out; }
  @keyframes draw-check { to { stroke-dashoffset: 0; } }
  .confetti { position: absolute; width: 8px; height: 12px; opacity: 0; animation: confetti-fall 2s ease-out forwards; }
  @keyframes confetti-fall { 0% { transform: translate(0,0) rotate(0); opacity: 1; } 100% { transform: translate(var(--tx), var(--ty)) rotate(var(--r)); opacity: 0; } }
  .toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(120px); background: rgba(255,94,58,0.95); color: white; padding: 12px 22px; border-radius: 12px; font-size: 14px; font-weight: 600; z-index: 1000; transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); box-shadow: 0 10px 30px -5px rgba(255,94,58,0.5); }
  .toast.show { transform: translateX(-50%) translateY(0); }
  .reveal { opacity: 0; transform: translateY(24px); transition: opacity 0.7s, transform 0.7s; }
  .reveal.visible { opacity: 1; transform: translateY(0); }
  .spinner { display: inline-block; width: 18px; height: 18px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; vertical-align: middle; margin-right: 8px; }
  @keyframes spin { to { transform: rotate(360deg); } }
  ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 3px; }
</style>
</head>
<body>
  <div class="bg-mesh"></div>
  <div class="bg-grid"></div>
  <div id="particles"></div>
  <main class="max-w-2xl mx-auto px-4 py-6">
    <header class="text-center pt-6 pb-10">
      <div class="tg-icon-wrap"><div class="tg-icon"><svg viewBox="0 0 24 24" fill="white" class="w-12 h-12"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg></div></div>
      <h1 class="display-font font-black text-2xl leading-tight mb-3">РАЗРАБОТКА МИНИ<br><span style="background: linear-gradient(135deg, #ff5e3a 0%, #ffb800 50%, #00d9c0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">ПРИЛОЖЕНИЙ</span><br>ДЛЯ ВАШЕГО БИЗНЕСА</h1>
      <p class="text-sm text-gray-400 max-w-md mx-auto">Заполните бриф — администратор свяжется с вами в Telegram в течение 15 минут</p>
    </header>
    <section class="card p-5 mb-4 reveal">
      <div class="flex items-center justify-between mb-5"><span class="section-label"><i class="fas fa-clipboard-list"></i> Шаг 1</span><span class="text-xs text-gray-500">Требования</span></div>
      <div class="mb-5"><label class="block text-sm font-semibold mb-3">Вид деятельности <span class="text-orange-400">*</span></label><div class="flex flex-wrap gap-2" id="businessTypes"></div></div>
      <div class="mb-5"><label class="block text-sm font-semibold mb-3">Тип приложения</label><div class="flex flex-wrap gap-2" id="appTypes"></div></div>
      <div class="mb-5"><label class="block text-sm font-semibold mb-3">Стиль дизайна <span class="text-orange-400">*</span></label><div class="grid grid-cols-2 gap-2" id="designStyles"></div></div>
      <div class="mb-5"><label class="block text-sm font-semibold mb-3">Цветовая гамма</label><div class="space-y-2" id="palettes"></div></div>
      <div class="mb-5"><label class="block text-sm font-semibold mb-3">Необходимый функционал</label><div class="flex flex-wrap gap-2" id="features"></div></div>
      <div class="mb-5"><label class="block text-sm font-semibold mb-3">Бюджет: <span id="budgetLabel" class="text-orange-400 font-bold">50 000 ₽</span></label><input type="range" id="budget" min="10000" max="500000" step="10000" value="50000"><div class="flex justify-between text-xs text-gray-500 mt-2"><span>10K ₽</span><span>500K+ ₽</span></div></div>
      <div class="mb-5"><label class="block text-sm font-semibold mb-3">Сроки запуска <span class="text-orange-400">*</span></label><div class="flex flex-wrap gap-2" id="timelines"></div></div>
      <div><label class="block text-sm font-semibold mb-2">Дополнительные пожелания</label><textarea class="input" id="comments" rows="3" placeholder="Опишите ваши идеи, референсы..."></textarea></div>
    </section>
    <section class="card p-5 mb-4 reveal">
      <div class="flex items-center justify-between mb-5"><span class="section-label"><i class="fas fa-user"></i> Шаг 2</span><span class="text-xs text-gray-500">Контакты</span></div>
      <div class="space-y-3">
        <div><label class="block text-sm font-semibold mb-2">Имя <span class="text-orange-400">*</span></label><input type="text" class="input" id="clientName" placeholder="Как к вам обращаться?"></div>
        <div><label class="block text-sm font-semibold mb-2">Телефон <span class="text-orange-400">*</span></label><input type="tel" class="input" id="clientPhone" placeholder="+7 (999) 123-45-67"></div>
        <div><label class="block text-sm font-semibold mb-2">Компания</label><input type="text" class="input" id="clientCompany" placeholder="Название компании (необязательно)"></div>
      </div>
    </section>
    <section class="card p-5 mb-4 reveal" id="summaryCard" style="display:none;"><div class="flex items-center gap-2 mb-3"><i class="fas fa-check-circle" style="color: var(--accent-2)"></i><span class="text-sm font-semibold">Ваш заказ</span></div><div id="summaryContent" class="text-sm text-gray-300 space-y-1"></div></section>
    <button class="btn-submit w-full reveal" id="submitBtn"><span id="submitText">Оформить заказ</span></button>
    <p class="text-center text-xs text-gray-500 mt-4 reveal">Нажимая кнопку, вы соглашаетесь на обработку персональных данных</p>
  </main>
  <div class="success-overlay" id="successOverlay">
    <div class="success-card card p-8 max-w-sm w-full text-center relative">
      <div id="confettiBox" class="absolute inset-0 overflow-hidden pointer-events-none"></div>
      <div class="checkmark-circle"><svg class="checkmark-svg" viewBox="0 0 24 24"><polyline points="4,12 10,18 20,6"></polyline></svg></div>
      <h2 class="display-font font-black text-2xl mb-2">Заказ принят!</h2>
      <p class="text-sm text-gray-400 mb-5">Спасибо за заявку.</p>
      <div class="rounded-xl p-3 mb-5" style="background: rgba(0,217,192,0.08); border: 1px solid rgba(0,217,192,0.2);"><div class="text-xs text-gray-500 mb-1">Номер заказа</div><div class="display-font font-bold text-lg" id="orderNumber" style="color: var(--accent-2)">—</div></div>
      <button class="btn-submit w-full" id="closeBtn"><span>Отлично</span></button>
    </div>
  </div>
  <div class="toast" id="toast"></div>

<script>
  const tg = window.Telegram?.WebApp;
  if (tg) { tg.expand(); tg.setHeaderColor('#0a0d14'); tg.setBackgroundColor('#0a0d14'); }

  const businessTypes = ['Ресторан / Кафе', 'Магазин', 'Услуги', 'Образование', 'Медицина', 'Фитнес', 'Недвижимость', 'Логистика', 'Другое'];
  const appTypes = ['Каталог', 'Доставка', 'Бронирование', 'Калькулятор', 'Личный кабинет', 'Запись на услугу', 'Магазин', 'Витрина', 'Другое'];
  const designStyles = [{ name: 'Минимал', preview: 'linear-gradient(135deg, #fff 0%, #e8e8e8 100%)' },{ name: 'Тёмный', preview: 'linear-gradient(135deg, #1a1a2e 0%, #0a0a0a 100%)' },{ name: 'Яркий', preview: 'linear-gradient(135deg, #ff5e3a 0%, #ffb800 100%)' },{ name: 'Корпоративный',preview: 'linear-gradient(135deg, #2aabee 0%, #229ed9 100%)' }];
  const palettes = [{ name: 'Оранжевый закат', colors: ['#ff5e3a', '#ffb800', '#fff5e6'] },{ name: 'Морская свежесть', colors: ['#00d9c0', '#2aabee', '#e8f4fd'] },{ name: 'Ночной город', colors: ['#1a1a2e', '#ff3d8a', '#f5f7fa'] },{ name: 'Природный', colors: ['#2d6a4f', '#95d5b2', '#fefae0'] }];
  const features = ['Корзина', 'Оплата онлайн', 'Уведомления', 'Чат с менеджером', 'Профиль', 'Поиск', 'Фильтры', 'Отзывы'];
  const timelines = ['Срочно (1-2 недели)', '1 месяц', '2 месяца', '3+ месяца'];
  const state = { businessType: null, appType: null, designStyle: null, palette: null, features: [], budget: 50000, timeline: null, comments: '', name: '', phone: '', company: '' };

  function renderChips(containerId, items, key, multi = false) { const c = document.getElementById(containerId); c.innerHTML = ''; items.forEach(item => { const el = document.createElement('div'); el.className = 'chip'; el.textContent = item; el.onclick = () => { if (!multi) { c.querySelectorAll('.chip').forEach(ch => ch.classList.remove('active')); el.classList.add('active'); state[key] = item; } else { el.classList.toggle('active'); if (el.classList.contains('active')) state[key].push(item); else state[key] = state[key].filter(i => i !== item); } tg?.HapticFeedback?.selectionChanged?.(); updateSummary(); }; c.appendChild(el); }); }
  
  function renderStyleCards() { const c = document.getElementById('designStyles'); c.innerHTML = ''; designStyles.forEach(s => { const el = document.createElement('div'); el.className = 'style-card'; el.innerHTML = `<div class="style-preview" style="background: ${s.preview}"></div><div class="text-sm font-semibold">${s.name}</div>`; el.onclick = () => { c.querySelectorAll('.style-card').forEach(x => x.classList.remove('active')); el.classList.add('active'); state.designStyle = s.name; tg?.HapticFeedback?.selectionChanged?.(); updateSummary(); }; c.appendChild(el); }); }
  
  function renderPalettes() { const c = document.getElementById('palettes'); c.innerHTML = ''; palettes.forEach(p => { const w = document.createElement('div'); w.className = 'flex items-center gap-3'; const pe = document.createElement('div'); pe.className = 'palette'; p.colors.forEach(col => { const d = document.createElement('div'); d.style.background = col; pe.appendChild(d); }); const l = document.createElement('div'); l.className = 'text-xs text-gray-400 w-32 flex-shrink-0'; l.textContent = p.name; pe.onclick = () => { c.querySelectorAll('.palette').forEach(x => x.classList.remove('active')); pe.classList.add('active'); state.palette = p.name; tg?.HapticFeedback?.selectionChanged?.(); updateSummary(); }; w.appendChild(pe); w.appendChild(l); c.appendChild(w); }); }

  renderChips('businessTypes', businessTypes, 'businessType'); renderChips('appTypes', appTypes, 'appType'); renderStyleCards(); renderPalettes(); renderChips('features', features, 'features', true); renderChips('timelines', timelines, 'timeline');

  const budgetInput = document.getElementById('budget');
  function updateBudgetVisual() { const pct = ((budgetInput.value - budgetInput.min) / (budgetInput.max - budgetInput.min)) * 100; budgetInput.style.setProperty('--val', pct + '%'); }
  budgetInput.oninput = (e) => { state.budget = parseInt(e.target.value); document.getElementById('budgetLabel').textContent = state.budget.toLocaleString('ru-RU') + ' ₽'; updateBudgetVisual(); updateSummary(); };
  updateBudgetVisual();
  document.getElementById('comments').oninput = e => state.comments = e.target.value;
  document.getElementById('clientName').oninput = e => { state.name = e.target.value; updateSummary(); };
  document.getElementById('clientPhone').oninput = e => { e.target.value = e.target.value.replace(/[^\d+]/g, ''); state.phone = e.target.value; updateSummary(); };
  document.getElementById('clientCompany').oninput = e => state.company = e.target.value;

  function updateSummary() { const card = document.getElementById('summaryCard'); const content = document.getElementById('summaryContent'); if (!state.businessType && !state.name) { card.style.display = 'none'; return; } card.style.display = 'block'; const items = []; if (state.businessType) items.push(row('Сфера', state.businessType)); if (state.appType) items.push(row('Тип', state.appType)); if (state.designStyle) items.push(row('Стиль', state.designStyle)); items.push(row('Бюджет', '~' + state.budget.toLocaleString('ru-RU') + ' ₽')); if (state.name) items.push(row('Клиент', state.name)); content.innerHTML = items.join(''); }
  function row(k, v) { return `<div class="flex justify-between gap-3"><span class="text-gray-500">${k}:</span><span class="text-right">${v}</span></div>`; }
  function showToast(msg) { const t = document.getElementById('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(t._timer); t._timer = setTimeout(() => t.classList.remove('show'), 3000); }

  document.getElementById('submitBtn').onclick = async () => {
    if (!state.businessType) return showToast('Укажите вид деятельности');
    if (!state.designStyle) return showToast('Выберите стиль дизайна');
    if (!state.timeline) return showToast('Укажите сроки запуска');
    if (!state.name || state.name.trim().length < 2) return showToast('Введите имя');
    if (!state.phone || state.phone.replace(/\D/g, '').length < 11) return showToast('Введите корректный номер телефона');

    const btn = document.getElementById('submitBtn'); const btnText = document.getElementById('submitText');
    btn.disabled = true; btnText.innerHTML = '<span class="spinner"></span>Отправляем...';

    const orderData = { orderId: 'MP-' + Date.now().toString(36).toUpperCase().slice(-6), ...state, timestamp: new Date().toISOString() };

    try {
      // ОТПРАВЛЯЕМ ДАННЫЕ НА НАШ СЕРВЕР (Render)
      const res = await fetch(`/api/submit-order`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      });
      if (!res.ok) throw new Error('Server error');
      showSuccess(orderData.orderId);
    } catch (err) {
      console.error(err);
      showToast('Ошибка сети. Попробуйте еще раз.');
    } finally {
      btn.disabled = false; btnText.textContent = 'Оформить заказ';
    }
  };

  function showSuccess(orderId) { document.getElementById('orderNumber').textContent = orderId; document.getElementById('successOverlay').classList.add('show'); const box = document.getElementById('confettiBox'); box.innerHTML = ''; const colors = ['#ff5e3a', '#00d9c0', '#ffb800', '#2aabee']; for(let i=0;i<20;i++){const c=document.createElement('div');c.className='confetti';c.style.background=colors[Math.floor(Math.random()*colors.length)];c.style.left='50%';c.style.top='30%';c.style.setProperty('--tx',(Math.random()-0.5)*300+'px');c.style.setProperty('--ty',(Math.random()*300+100)+'px');c.style.setProperty('--r',(Math.random()*720-360)+'deg');c.style.animationDelay=Math.random()*0.3+'s';box.appendChild(c);} tg?.HapticFeedback?.notificationOccurred('success'); }
  document.getElementById('closeBtn').onclick = () => { document.getElementById('successOverlay').classList.remove('show'); if (tg?.close) tg.close(); };

  const pColors = ['#ff5e3a', '#00d9c0', '#ffb800']; const pBox = document.getElementById('particles'); for (let i = 0; i < 15; i++) { const p = document.createElement('div'); p.className = 'particle'; p.style.left = Math.random() * 100 + '%'; const c = pColors[Math.floor(Math.random() * pColors.length)]; p.style.background = c; p.style.boxShadow = `0 0 10px ${c}`; p.style.animationDuration = (Math.random() * 12 + 12) + 's'; p.style.animationDelay = -Math.random() * 20 + 's'; pBox.appendChild(p); }
  const io = new IntersectionObserver((entries) => { entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }); }, { threshold: 0.1 }); document.querySelectorAll('.reveal').forEach(el => io.observe(el));
</script>
</body>
</html>
"""

# ----------------------------------- ПУТИ FASTAPI -----------------------------------

# 1. Главная страница (Отдаем HTML приложение)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content

# 2. ЭНДПОИНТ ДЛЯ ПРИЕМА ЗАЯВКИ ОТ ФРОНТЕНДА
@app.post("/api/submit-order")
async def submit_order(request: Request):
    # Получаем данные от сайта
    data = await request.json()
    
    # Формируем красивое сообщение для вас
    msg_text = f"""
🆕 <b>НОВЫЙ ЗАКАЗ {data.get('orderId', 'Ошибка')}</b>

📋 <b>БРИФ ЗАКАЗЧИКА</b>
• Сфера: <b>{data.get('businessType', '—')}</b>
• Тип: <b>{data.get('appType', '—')}</b>
• Стиль: <b>{data.get('designStyle', '—')}</b>
• Палитра: <b>{data.get('palette', '—')}</b>
• Функции: {', '.join(data.get('features', [])) or '—'}
• Сроки: <b>{data.get('timeline', '—')}</b>
• Бюджет: <b>~{data.get('budget', 0):,} ₽</b>

👤 <b>ДАННЫЕ КЛИЕНТА</b>
• Имя: <b>{data.get('name', '—')}</b>
• Телефон: <b>{data.get('phone', '—')}</b>
• Компания: {data.get('company', '—')}

💬 <b>ПОЖЕЛАНИЯ</b>
{data.get('comments', '—')}
"""
    
    # ОТПРАВЛЯЕМ ВАМ В ЛИЧКУ (ID 664576828)
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=msg_text, parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка отправки админу: {e}")
    
    # Возвращаем фронтенду статус "ОК"
    return {"status": "ok"}

# 3. Вебхук для самого Telegram бота (чтобы бот не спал и мог получать команды)
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}
