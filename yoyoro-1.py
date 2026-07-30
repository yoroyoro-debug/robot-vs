<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ロボットバトルアリーナ - Web Edition</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0F172A; color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; justify-content: center; padding: 16px; min-height: 100vh; }
        .container { width: 100%; max-width: 480px; display: flex; flex-direction: column; gap: 14px; }
        .header { background: #1E293B; border-radius: 14px; padding: 12px 18px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155; }
        .title { color: #38BDF8; font-size: 18px; font-weight: bold; }
        .round { color: #A855F7; font-size: 14px; font-weight: bold; }
        
        .card { background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-radius: 16px; padding: 16px; border: 2px solid #334155; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 12px rgba(0,0,0,0.4); }
        .card-enemy { border-color: #A855F7; box-shadow: 0 0 15px rgba(168, 85, 247, 0.15); }
        .card-player { border-color: #38BDF8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.15); }
        .card-info { flex: 1; }
        .label { font-size: 11px; font-weight: bold; color: #94A3B8; text-transform: uppercase; }
        .name { font-size: 18px; font-weight: bold; color: #FFFFFF; margin: 2px 0 6px 0; }
        
        .hp-bar-bg { background: #334155; border-radius: 10px; height: 12px; overflow: hidden; margin-bottom: 4px; }
        .hp-bar-fill { background: #22C55E; height: 100%; width: 100%; transition: width 0.3s ease; }
        .hp-enemy { background: #F43F5E; }
        .hp-text { font-size: 13px; font-weight: bold; }
        
        .robot-icon { width: 64px; height: 64px; opacity: 0.9; }

        .vs-badge { text-align: center; font-size: 12px; font-weight: bold; color: #64748B; letter-spacing: 2px; }

        .btn { background: #38BDF8; color: #0F172A; font-weight: bold; font-size: 16px; border: none; padding: 14px; border-radius: 12px; cursor: pointer; transition: transform 0.1s, background 0.2s; width: 100%; text-align: center; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3); }
        .btn:active { transform: scale(0.97); }
        .btn-attack { background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%); color: white; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.4); }
        
        .control-card { background: #1E293B; border-radius: 16px; padding: 16px; border: 1px solid #334155; text-align: center; display: flex; flex-direction: column; gap: 12px; }
        .status-msg { font-size: 15px; font-weight: bold; color: #F8FAFC; }
        
        .logs-box { background: #020617; border-radius: 10px; padding: 10px; max-height: 120px; overflow-y: auto; font-family: monospace; font-size: 11px; color: #CBD5E1; display: flex; flex-direction: column; gap: 4px; border: 1px solid #1E293B; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="title">🤖 ROBO BATTLE ARENA</div>
            <div id="round-text" class="round">ROUND 1</div>
        </div>

        <!-- Enemy Card -->
        <div class="card card-enemy">
            <div class="card-info">
                <div class="label" style="color: #A855F7;">ライバルロボ</div>
                <div class="name">ブラックライトニング</div>
                <div class="hp-bar-bg"><div id="enemy-hp-bar" class="hp-bar-fill hp-enemy"></div></div>
                <div id="enemy-hp-text" class="hp-text" style="color: #F43F5E;">HP: 300 / 300</div>
            </div>
            <img class="robot-icon" src="https://api.iconify.design/game-icons:robot-antennas.svg?color=%23a855f7" alt="Enemy Robot">
        </div>

        <div class="vs-badge">⚡ VS BATTLE ⚡</div>

        <!-- Player Card -->
        <div class="card card-player">
            <div class="card-info">
                <div class="label" style="color: #38BDF8;">マイロボ</div>
                <div class="name">ドラコニック インパクト</div>
                <div class="hp-bar-bg"><div id="player-hp-bar" class="hp-bar-fill"></div></div>
                <div id="player-hp-text" class="hp-text" style="color: #22C55E;">HP: 300 / 300</div>
            </div>
            <img class="robot-icon" src="https://api.iconify.design/game-icons:mech-golem.svg?color=%2338bdf8" alt="Player Robot">
        </div>

        <!-- Interactive Control -->
        <div class="control-card">
            <div id="status-text" class="status-msg">対戦を開始してください</div>
            <button id="action-btn" class="btn" onclick="handleAction()">🚀 バトルスタート！</button>
        </div>

        <!-- Logs -->
        <div class="control-card" style="padding: 12px;">
            <div class="label" style="text-align: left; margin-bottom: 6px;">📜 戦闘ログ</div>
            <div id="logs" class="logs-box"><div>[System] ゲーム準備完了。</div></div>
        </div>
    </div>

    <script>
        let pHP = 300, eHP = 300, round = 1, taps = 0, phase = "READY", timer = 10.0, timerId = null;
        const roulettes = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180];

        function updateUI() {
            document.getElementById("round-text").innerText = `ROUND ${round}`;
            document.getElementById("player-hp-bar").style.width = (pHP / 300 * 100) + "%";
            document.getElementById("player-hp-text").innerText = `HP: ${pHP} / 300`;
            document.getElementById("enemy-hp-bar").style.width = (eHP / 300 * 100) + "%";
            document.getElementById("enemy-hp-text").innerText = `HP: ${eHP} / 300`;
        }

        function addLog(tag, msg) {
            const logs = document.getElementById("logs");
            logs.innerHTML = `<div>[${tag}] ${msg}</div>` + logs.innerHTML;
        }

        function handleAction() {
            const btn = document.getElementById("action-btn");
            const st = document.getElementById("status-text");

            if (phase === "READY" || phase === "GAME_OVER") {
                pHP = 300; eHP = 300; round = 1; taps = 0; phase = "PLAYER_ATTACK"; timer = 10.0;
                updateUI();
                btn.className = "btn btn-attack";
                btn.innerText = "⚔️ 限界突破ラッシュ！ (連打！)";
                
                timerId = setInterval(() => {
                    timer -= 0.1;
                    st.innerText = `⏱️ 残り時間: ${Math.max(0, timer).toFixed(1)}s | 連打数: ${taps}`;
                    if (timer <= 0) {
                        clearInterval(timerId);
                        finishPlayerAttack();
                    }
                }, 100);
            } else if (phase === "PLAYER_ATTACK") {
                taps++;
                st.innerText = `⏱️ 残り時間: ${Math.max(0, timer).toFixed(1)}s | 連打数: ${taps}`;
            } else if (phase === "PLAYER_RESULT") {
                executeEnemyTurn();
            } else if (phase === "ENEMY_RESULT") {
                phase = "PLAYER_ATTACK"; taps = 0; timer = 10.0;
                btn.className = "btn btn-attack";
                btn.innerText = "⚔️ 限界突破ラッシュ！ (連打！)";
                timerId = setInterval(() => {
                    timer -= 0.1;
                    st.innerText = `⏱️ 残り時間: ${Math.max(0, timer).toFixed(1)}s | 連打数: ${taps}`;
                    if (timer <= 0) {
                        clearInterval(timerId);
                        finishPlayerAttack();
                    }
                }, 100);
            }
        }

        function finishPlayerAttack() {
            const btn = document.getElementById("action-btn");
            const st = document.getElementById("status-text");
            const dmg = taps * 2;
            eHP = Math.max(0, eHP - dmg);
            updateUI();
            addLog("Player", `ROUND ${round}: ${taps}連打！ ${dmg} ダメージ！`);

            if (eHP <= 0) {
                phase = "GAME_OVER";
                st.innerText = "🎉 WINNER! 敵ロボを撃破しました！";
                btn.className = "btn";
                btn.innerText = "🔄 もう一度対戦する";
            } else {
                phase = "PLAYER_RESULT";
                st.innerText = `攻撃結果: ${taps}連打 (${dmg}ダメージ！)`;
                btn.className = "btn";
                btn.innerText = "次へ (敵の攻撃ターン)";
            }
        }

        function executeEnemyTurn() {
            const btn = document.getElementById("action-btn");
            const st = document.getElementById("status-text");
            const eDmg = roulettes[Math.floor(Math.random() * roulettes.length)];
            pHP = Math.max(0, pHP - eDmg);
            updateUI();
            addLog("Enemy", `ROUND ${round}: ルーレット [${eDmg}]！ ${eDmg} 被ダメージ！`);

            if (pHP <= 0) {
                phase = "GAME_OVER";
                st.innerText = "💥 GAME OVER... プレイヤーロボ大破";
                btn.className = "btn btn-attack";
                btn.innerText = "🔄 リトライする";
            } else {
                round++;
                phase = "ENEMY_RESULT";
                st.innerText = `敵の攻撃: ${eDmg} ダメージを受けた！`;
                btn.className = "btn";
                btn.innerText = "次へ (自分の攻撃ターン)";
            }
        }
    </script>
</body>
</html>
