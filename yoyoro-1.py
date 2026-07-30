# =========================================================
# Robot Battle Game - Streamlit Edition (app.py)
# =========================================================
import streamlit as st
import random
import time

# --- 1. Game State Management ---
if "game_state" not in st.session_state:
    class GameState:
        def __init__(self):
            self.reset()

        def reset(self):
            self.player_hp = 1000
            self.max_player_hp = 1000
            self.enemy_hp = 1000
            self.max_enemy_hp = 1000
            self.round_count = 1
            self.selected_time = 20
            self.phase = "PLAYER_ATTACK"
            self.tap_count = 0
            self.last_player_damage = 0
            self.last_enemy_damage = 0
            self.battle_logs = ["バトル準備完了！ ドラゴニックVSライトニングの対戦を開始してください。"]
            self.roulette_numbers = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]

        def add_log(self, tag, msg):
            self.battle_logs.insert(0, f"[{tag}] {msg}")

        def tap_attack(self):
            if self.phase == "PLAYER_ATTACK":
                self.tap_count += 1

        def finish_player_attack(self):
            mult = 1 if self.selected_time == 20 else 2
            self.last_player_damage = self.tap_count * mult
            self.enemy_hp = max(0, self.enemy_hp - self.last_player_damage)
            self.add_log("Dragonic", f"ROUND {self.round_count}: {self.selected_time}秒間で {self.tap_count}連打！ 相手に {self.last_player_damage} ダメージ！")
            
            if self.enemy_hp <= 0:
                self.phase = "GAME_OVER"
            else:
                self.phase = "PLAYER_RESULT"

        def execute_enemy_turn(self):
            self.last_enemy_damage = random.choice(self.roulette_numbers)
            self.player_hp = max(0, self.player_hp - self.last_enemy_damage)
            self.add_log("Lightning", f"ROUND {self.round_count}: ライバルロボの攻撃 [{self.last_enemy_damage}]！ {self.last_enemy_damage} 被ダメージ！")

            if self.player_hp <= 0:
                self.phase = "GAME_OVER"
            else:
                self.phase = "ENEMY_RESULT"

        def next_round(self):
            self.round_count += 1
            self.tap_count = 0
            self.phase = "PLAYER_ATTACK"

    st.session_state.game_state = GameState()

game = st.session_state.game_state

# --- 2. Streamlit Custom Styled UI ---
def main():
    st.set_page_config(page_title="ドラゴニック VS ライトニング バトル", page_icon="🤖", layout="centered")

    # Custom Cyberpunk / Dark UI CSS
    st.markdown('''
    <style>
    .main {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: bold;
        font-size: 16px;
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    .title-bar {
        background: #1E293B;
        padding: 12px 20px;
        border-radius: 16px;
        border: 1px solid #334155;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .card-enemy {
        background: #2E1065;
        border: 2px solid #A855F7;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .card-player {
        background: #0C4A6E;
        border: 2px solid #38BDF8;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .hp-text-enemy { color: #E9D5FF; font-weight: bold; font-size: 18px; }
    .hp-text-player { color: #BAE6FD; font-weight: bold; font-size: 18px; }
    </style>
    ''', unsafe_allow_html=True)

    # Title Bar
    st.markdown(f'''
    <div class="title-bar">
        <span style="font-size: 20px; font-weight: bold; color: #38BDF8;">🤖 ROBOT BATTLE ARENA</span>
        <span style="font-size: 16px; font-weight: bold; color: #A855F7;">ROUND {game.round_count}</span>
    </div>
    ''', unsafe_allow_html=True)

    # Robot Cards Area
    col_e1, col_e2 = st.columns([3, 1])
    with col_e1:
        st.markdown(f'''
        <div class="card-enemy">
            <div>
                <div style="font-size: 12px; color: #A855F7; font-weight: bold;">ライバルロボ</div>
                <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">ブラックライトニング</div>
                <div class="hp-text-enemy">HP {game.enemy_hp} / {game.max_enemy_hp}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with col_e2:
        st.markdown("<h1 style='text-align: center;'>⚡</h1>", unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.markdown(f'''
        <div class="card-player">
            <div>
                <div style="font-size: 12px; color: #38BDF8; font-weight: bold;">マイロボ</div>
                <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">ドラゴニック インパクト</div>
                <div class="hp-text-player">HP {game.player_hp} / {game.max_player_hp}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with col_p2:
        st.markdown("<h1 style='text-align: center;'>🐉</h1>", unsafe_allow_html=True)

    st.divider()

    # --- Game Phase Logic & Controls ---
    if game.phase == "PLAYER_ATTACK":
        st.subheader("⚔️ あなたのターン: 連打攻撃！")
        time_choice = st.radio("制限時間を選択", [20, 10], horizontal=True, index=0 if game.selected_time == 20 else 1)
        game.selected_time = time_choice

        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            if st.button("🔥 連打攻撃！！", use_container_width=True):
                game.tap_attack()

        dmg_per_tap = 1 if game.selected_time == 20 else 2
        st.metric("現在の連打数", f"{game.tap_count} 回", f"与ダメージ: {game.tap_count * dmg_per_tap}")

        if st.button("⏱️ 攻撃確定 (ターン終了)", use_container_width=True, type="primary"):
            game.finish_player_attack()
            st.rerun()

    elif game.phase == "PLAYER_RESULT":
        st.success(f"💥 攻撃完了！ {game.last_player_damage} ダメージを与えた！")
        if st.button("次へ (ライバルロボのターン)", use_container_width=True):
            game.execute_enemy_turn()
            st.rerun()

    elif game.phase == "ENEMY_RESULT":
        st.error(f"⚡ ライバルロボのこうげき！ {game.last_enemy_damage} ダメージを受けた！")
        if st.button("次へ (ドラゴニックのターン)", use_container_width=True):
            game.next_round()
            st.rerun()

    elif game.phase == "GAME_OVER":
        if game.player_hp > 0:
            st.balloons()
            st.success("🎉 VICTORY! あなたの勝利です！")
        else:
            st.error("💀 GAME OVER... ライバルロボに敗北しました")

        if st.button("🔄 もう一度対戦する", use_container_width=True):
            game.reset()
            st.rerun()

    # Battle Logs Section
    st.divider()
    st.subheader("📜 バトルログ")
    for log in game.battle_logs:
        st.text(log)

if __name__ == "__main__":
    main()
