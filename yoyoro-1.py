import streamlit as st
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(
    page_title="サイバーヒーローVS暗黒龍王",
    page_icon="🦸‍♂️",
    layout="centered"
)

# 完全作動するHTML/CSS/JS埋め込みコード
html_code = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ヒーローVS大怪獣 バトルアリーナ</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0F172A; color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; justify-content: center; padding: 12px; min-height: 100vh; }
        
        .container { width: 100%; max-width: 420px; display: flex; flex-direction: column; gap: 12px; }
        
        .header { display: flex; justify-content: space-between; align-items: center; background: #1E293B; padding: 12px 16px; border-radius: 12px; border: 1px solid #334155; }
        .title { font-size: 16px; font-weight: bold; color: #38BDF8; }
        .round { font-size: 14px; font-weight: bold; color: #A855F7; }

        .card { background: #1E293B; border-radius: 16px; padding: 14px; border: 2px solid #334155; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }
        .card-enemy { border-color: #A855F7; box-shadow: 0 0 15px rgba(168, 85, 247, 0.2); }
        .card-player { border-color: #38BDF8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }

        .card-info { display: flex; flex-direction: column; gap: 4px; flex: 1; }
        .label { font-size: 11px; font-weight: bold; text-transform: uppercase; }
        .name { font-size: 17px; font-weight: bold; color: #FFFFFF; }
        
        .hp-bar-bg { background: #0F172A; height: 10px; border-radius: 5px; width: 100%; overflow: hidden; margin-top: 4px; border: 1px solid #334155; }
        .hp-bar-fill { height: 100%; width: 100%; transition: width 0.3s ease; background: #22C55E; }
        .hp-enemy { background: #F43F5E; }
        .hp-text { font-size: 12px; font-weight: bold; }
        
        .char-avatar { font-size: 42px; width: 56px; text-align: center; }

        .vs-badge { text-align: center; font-size: 12px; font-weight: bold; color: #64748B; letter-spacing: 2px; }

        .time-select-group { display: flex; gap: 10px; margin-bottom: 8px; }
        .time-btn { flex: 1; padding: 8px; border-radius: 10px; border: 1px solid #334155; background: #0F172A; color: #94A3B8; font-weight: bold; cursor: pointer; }
        .time-btn.active { background: #38BDF8; color: #0F172A; border-color: #38BDF8; }

        .btn { background: #38BDF8; color: #0F172A; font-weight: bold; font-size: 16px; border: none; padding: 14px; border-radius: 12px; cursor: pointer; transition: transform 0.1s, background 0.2s; width: 100%; text-align: center; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3); }
        .btn:active { transform: scale(0.96); }
        .btn-attack { background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%); color: white; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.4); font-size: 18px; }
        
        .control-card { background: #1E293B; border-radius: 16px; padding: 16px; border: 1px solid #334155; text-align: center; display: flex; flex-direction: column; gap: 10px; }
        .status-msg { font-size: 15px; font-weight: bold; color: #F8FAFC; }
        .timer-display { font-size: 22px; font-weight: 900; color: #38BDF8; margin-top: 2px; }

        .logs-box { background: #020617; border-radius: 10px; padding: 10px; max-height: 110px; overflow-y: auto; font-family: monospace; font-size: 11px; color: #CBD5E1; display: flex; flex-direction: column; gap: 4px; border: 1px solid #1E293B; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">🦸‍♂️ サイバーヒーロー VS 暗黒龍王</div>
            <div id="round-text" class="round">ROUND 1</div>
        </div>

        <!-- Enemy Kaiju Card -->
        <div class="card card-enemy">
            <div class="card-info">
                <div class="label" style="color: #A855F7;">だいかいじゅう</div>
                <div class="name">暗黒龍王 ギガガメディス</div>
                <div class="hp-bar-bg"><div id="enemy-hp-bar" class="hp-bar-fill hp-enemy"></div></div>
                <div id="enemy-hp-text" class="hp-text" style="color: #F43F5E;">HP: 300 / 300</div>
            </div>
            <div class="char-avatar">🐉</div>
        </div>

        <div class="vs-badge">🔥 HERO VS KAIJU 🔥</div>

        <!-- Player Hero Card -->
        <div class="card card-player">
            <div class="card-info">
                <div class="label" style="color: #38BDF8;">マイヒーロー</div>
                <div class="name">サイバーヒーロー・ブレイバー</div>
                <div class="hp-bar-bg"><div id="player-hp-bar" class="hp-bar-fill"></div></div>
                <div id="player-hp-text" class="hp-text" style="color: #22C55E;">HP: 300 / 300</div>
            </div>
            <div class="char-avatar">🦸‍♂️</div>
        </div>

        <!-- Interactive Control -->
        <div class="control-card">
            <div id="time-select-area">
                <div class="label" style="margin-bottom: 6px;">⏱️ たいせんじかんをえらぼう</div>
                <div class="time-select-group">
                    <button id="btn-time-10" class="time-btn active" onclick="selectTime(10)">⚡ 10秒コース</button>
                    <button id="btn-time-20" class="time-btn" onclick="selectTime(20)">🔥 20秒コース</button>
                </div>
            </div>
            <div id="status-text" class="status-msg">対戦を開始してください</div>
            <div id="timer-text" class="timer-display" style="display: none;">のこりじかん: 10.0秒</div>
            <button id="action-btn" class="btn" onclick="handleAction()">🚀 ヒーローバトルスタート！</button>
        </div>

        <!-- Logs -->
        <div>
            <div class="label" style="text-align: left; margin-bottom: 6px;">📜 戦闘ログ</div>
            <div id="logs" class="logs-box"><div>[System] バトル準備完了。</div></div>
        </div>
    </div>

    <script>
        let pHP = 300, eHP = 300, round = 1, taps = 0, phase = "READY", timer = 10.0, timeLimit = 10, timerId = null;
        const roulettes = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180];

        function playWebHitSound() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(180, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(30, ctx.currentTime + 0.08);
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.08);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.08);
            } catch (e) {}
        }

        function selectTime(sec) {
            if (phase !== "READY") return;
            timeLimit = sec;
            document.getElementById("btn-time-10").className = sec === 10 ? "time-btn active" : "time-btn";
            document.getElementById("btn-time-20").className = sec === 20 ? "time-btn active" : "time-btn";
        }

        function updateUI() {
            document.getElementById("round-text").innerText = `ROUND ${round}`;
            document.getElementById("player-hp-bar").style.width = (pHP / 300 * 100) + "%";
            document.getElementById("player-hp-text").innerText = `HP: ${pHP} / 300`;
            document.getElementById("enemy-hp-bar").style.width = (eHP / 300 * 100) + "%";
            document.getElementById("enemy-hp-text").innerText = `HP: ${eHP} / 300`;
        }

        function addLog(tag, msg) {
            const box = document.getElementById("logs");
            const div = document.createElement("div");
            div.innerText = `[${tag}] ${msg}`;
            box.prepend(div);
        }

        function handleAction() {
            const btn = document.getElementById("action-btn");
            const st = document.getElementById("status-text");
            const timerTxt = document.getElementById("timer-text");
            const timeArea = document.getElementById("time-select-area");

            if (phase === "READY" || phase === "GAME_OVER") {
                if (phase === "GAME_OVER") { pHP = 300; eHP = 300; round = 1; }
                taps = 0; phase = "PLAYER_ATTACK"; timer = timeLimit;
                updateUI();
                timeArea.style.display = "none";
                timerTxt.style.display = "block";
                btn.className = "btn btn-attack";
                btn.innerText = "💥 ヒーロービームアタック！ (連打！)";
                st.innerText = "🔥 ボタンを連打して大怪獣をたおせ！";
                
                if (timerId) clearInterval(timerId);
                timerId = setInterval(() => {
                    timer -= 0.1;
                    if (timer <= 0) {
                        timer = 0;
                        clearInterval(timerId);
                        finishPlayerAttack();
                    } else {
                        timerTxt.innerText = `のこりじかん: ${timer.toFixed(1)}秒 | 連打数: ${taps}`;
                    }
                }, 100);
            } else if (phase === "PLAYER_ATTACK") {
                if (timer > 0) {
                    taps++;
                    playWebHitSound();
                    timerTxt.innerText = `のこりじかん: ${Math.max(0, timer).toFixed(1)}秒 | 連打数: ${taps}`;
                }
            } else if (phase === "PLAYER_RESULT") {
                executeEnemyTurn();
            } else if (phase === "ENEMY_RESULT") {
                phase = "PLAYER_ATTACK";
                taps = 0; timer = timeLimit;
                btn.className = "btn btn-attack";
                btn.innerText = "💥 ヒーロービームアタック！ (連打！)";
                st.innerText = "🔥 ボタンを連打して大怪獣をたおせ！";
                timerTxt.style.display = "block";
                if (timerId) clearInterval(timerId);
                timerId = setInterval(() => {
                    timer -= 0.1;
                    if (timer <= 0) {
                        timer = 0;
                        clearInterval(timerId);
                        finishPlayerAttack();
                    } else {
                        timerTxt.innerText = `のこりじかん: ${timer.toFixed(1)}秒 | 連打数: ${taps}`;
                    }
                }, 100);
            }
        }

        function finishPlayerAttack() {
            const btn = document.getElementById("action-btn");
            const st = document.getElementById("status-text");
            const timerTxt = document.getElementById("timer-text");

            const damage = taps * 2;
            eHP = Math.max(0, eHP - damage);
            updateUI();
            addLog("Hero", `ROUND ${round}: ${timeLimit}秒間で ${taps}連打！ 大怪獣に ${damage} ダメージ！`);

            timerTxt.style.display = "none";

            if (eHP <= 0) {
                phase = "GAME_OVER";
                st.innerText = "🎉 WINNER! 大怪獣『ギガガメディス』を撃退した！";
                btn.className = "btn";
                btn.innerText = "🔄 もう一度対戦する";
                document.getElementById("time-select-area").style.display = "block";
            } else {
                phase = "PLAYER_RESULT";
                st.innerText = `💥 ヒーロー攻撃完了！ ${damage} ダメージを与えた！`;
                btn.className = "btn";
                btn.innerText = "次へ (大怪獣のターン)";
            }
        }

        function executeEnemyTurn() {
            const btn = document.getElementById("action-btn");
            const st = document.getElementById("status-text");

            const damage = roulettes[Math.floor(Math.random() * roulettes.length)];
            pHP = Math.max(0, pHP - damage);
            updateUI();
            addLog("Kaiju", `ROUND ${round}: 大怪獣の攻撃 [${damage}]！ ${damage} 被ダメージ！`);

            if (pHP <= 0) {
                phase = "GAME_OVER";
                st.innerText = "💥 GAME OVER... 超ヒーロー・ブレイバー倒れる";
                btn.className = "btn";
                btn.innerText = "🔄 もう一度対戦する";
                document.getElementById("time-select-area").style.display = "block";
            } else {
                phase = "ENEMY_RESULT";
                round++;
                st.innerText = `⚡ 大怪獣のルーレット攻撃！ ${damage} ダメージを受けた！`;
                btn.className = "btn";
                btn.innerText = "次へ (ヒーローのターン)";
            }
        }
    </script>
</body>
</html>
"""

# HTMLを埋め込んで表示
components.html(html_code, height=750, scrolling=False)
