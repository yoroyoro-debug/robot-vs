# =========================================================
# ヒーローVS大怪獣 バトルアリーナ (app.py)
# 
# 1. pip install streamlit
# 2. streamlit run app.py
# =========================================================

import streamlit as st
import random

# --- 1. Pure State Logic ---
class RobotBattleCore:
    def __init__(self):
        self.player_hp = 300
        self.max_player_hp = 300
        self.enemy_hp = 300
        self.max_enemy_hp = 300

        self.selected_time = 10  # 10 or 20 seconds
        self.round_count = 1
        self.phase = "READY"  # READY, PLAYER_ATTACK, PLAYER_RESULT, ENEMY_RESULT, GAME_OVER
        self.tap_count = 0
        self.last_player_damage = 0
        self.last_enemy_damage = 0
        self.battle_logs = ["バトル準備完了！ ヒーローVS大怪獣の対戦を開始してください。"]
        self.roulette_numbers = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]

    def add_log(self, tag, msg):
        self.battle_logs.insert(0, f"[{tag}] {msg}")

    def tap_attack(self):
        if self.phase == "PLAYER_ATTACK":
            self.tap_count += 1

    def finish_player_attack(self):
        self.last_player_damage = self.tap_count * 2
        self.enemy_hp = max(0, self.enemy_hp - self.last_player_damage)
        self.add_log("Hero", f"ROUND {self.round_count}: {self.selected_time}秒間で {self.tap_count}連打！ 大怪獣に {self.last_player_damage} ダメージ！")
        
        if self.enemy_hp <= 0:
            self.phase = "GAME_OVER"
        else:
            self.phase = "PLAYER_RESULT"

    def execute_enemy_turn(self):
        self.last_enemy_damage = random.choice(self.roulette_numbers)
        self.player_hp = max(0, self.player_hp - self.last_enemy_damage)
        self.add_log("Kaiju", f"ROUND {self.round_count}: 大怪獣の攻撃 [{self.last_enemy_damage}]！ {self.last_enemy_damage} ダメージを受けた！")

        if self.player_hp <= 0:
            self.phase = "GAME_OVER"
        else:
            self.phase = "ENEMY_RESULT"
            self.round_count += 1

    def reset_game(self):
        time_limit = self.selected_time
        self.__init__()
        self.selected_time = time_limit

# --- 2. Streamlit Custom Styled UI ---
def main():
    st.set_page_config(page_title="ヒーローVS大怪獣 バトルアリーナ", page_icon="🦸‍♂️", layout="centered")

    # Custom Cyberpunk / Dark UI CSS
    st.markdown('''
    <style>
        .stApp { background-color: #0F172A !important; color: #F8FAFC; }
        .robo-card {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border-radius: 16px;
            padding: 16px;
            border: 2px solid #334155;
            margin-bottom: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .enemy-card { border-color: #A855F7; box-shadow: 0 0 15px rgba(168, 85, 247, 0.2); }
        .player-card { border-color: #38BDF8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
        .hp-text-enemy { color: #F43F5E; font-weight: bold; font-size: 18px; }
        .hp-text-player { color: #22C55E; font-weight: bold; font-size: 18px; }
        .title-bar {
            background: #1E293B;
            border-radius: 12px;
            padding: 12px 20px;
            border: 1px solid #334155;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .stButton>button {
            border-radius: 12px !important;
            font-weight: bold !important;
            font-size: 18px !important;
            padding: 12px 24px !important;
            transition: all 0.2s !important;
        }
        .char-icon { font-size: 50px; text-align: center; }
    </style>
    ''', unsafe_allow_html=True)

    if "game" not in st.session_state:
        st.session_state.game = RobotBattleCore()

    game = st.session_state.game

    # Title Bar
    st.markdown(f'''
    <div class="title-bar">
        <span style="font-size: 20px; font-weight: bold; color: #38BDF8;">🦸‍♂️ HERO VS KAIJU BATTLE</span>
        <span style="font-size: 16px; font-weight: bold; color: #A855F7;">ROUND {game.round_count}</span>
    </div>
    ''', unsafe_allow_html=True)

    # Robot Cards Area (Enemy Kaiju Top, Player Hero Bottom)
    col_e1, col_e2 = st.columns([3, 1])
    with col_e1:
        st.markdown(f'''
        <div class="robo-card enemy-card">
            <div>
                <div style="font-size: 12px; color: #A855F7; font-weight: bold;">だいかいじゅう</div>
                <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">大怪獣 ギガガメディス</div>
                <div class="hp-text-enemy">HP {game.enemy_hp} / {game.max_enemy_hp}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.progress(game.enemy_hp / game.max_enemy_hp)
    with col_e2:
        st.markdown('<div class="char-icon">🦖</div>', unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; font-weight: bold; color: #64748B; margin: 8px 0;'>🔥 HERO VS KAIJU 🔥</div>", unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.markdown(f'''
        <div class="robo-card player-card">
            <div>
                <div style="font-size: 12px; color: #38BDF8; font-weight: bold;">マイヒーロー</div>
                <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">サイバーヒーロー・ブレイバー</div>
                <div class="hp-text-player">HP {game.player_hp} / {game.max_player_hp}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        st.progress(game.player_hp / game.max_player_hp)
    with col_p2:
        st.markdown('<div class="char-icon">🦸‍♂️</div>', unsafe_allow_html=True)

    st.divider()

    # Dynamic Battle Action Controls
    if game.phase == "READY":
        st.subheader("⏱️ 対戦時間を選んでバトルスタート！")
        selected_time = st.radio("制限時間を選択してください", [10, 20], index=0 if game.selected_time == 10 else 1, format_func=lambda x: f"⚡ {x}秒コース", horizontal=True)
        game.selected_time = selected_time

        if st.button(f"🚀 バトルスタート ({game.selected_time}秒連打)", use_container_width=True, type="primary"):
            game.phase = "PLAYER_ATTACK"
            game.tap_count = 0
            st.rerun()

    elif game.phase == "PLAYER_ATTACK":
        st.warning(f"🔥 {game.selected_time}秒間 ヒーロー連打アタック！ ボタンを押しまくれ！")
        if st.button("💥 ヒーロービームアタック！ (+1)", use_container_width=True):
            game.tap_attack()

        st.metric("現在の連打数", f"{game.tap_count} 回", f"与ダメージ: {game.tap_count * 2}")

        if st.button("⏱️ 攻撃確定 (ターン終了)", use_container_width=True, type="primary"):
            game.finish_player_attack()
            st.rerun()

    elif game.phase == "PLAYER_RESULT":
        st.success(f"💥 攻撃完了！ {game.last_player_damage} ダメージを与えた！")
        if st.button("次へ (大怪獣のターン)", use_container_width=True):
            game.execute_enemy_turn()
            st.rerun()

    elif game.phase == "ENEMY_RESULT":
        st.error(f"⚡ 大怪獣のこうげき！ {game.last_enemy_damage} ダメージを受けた！")
        if st.button("次へ (ヒーローのターン)", use_container_width=True):
            game.phase = "PLAYER_ATTACK"
            game.tap_count = 0
            st.rerun()

    elif game.phase == "GAME_OVER":
        if game.player_hp > 0:
            st.balloons()
            st.success("🎉 WINNER! 大怪獣『ギガガメディス』を撃退した！")
        else:
            st.error("💥 GAME OVER... 超ヒーロー・ブレイバー倒れる")

        if st.button("🔄 もう一度対戦する", use_container_width=True, type="primary"):
            game.reset_game()
            st.rerun()

    st.divider()
    st.caption("📜 戦闘ログ")
    for log in game.battle_logs[:6]:
        st.code(log, language="text")

if __name__ == "__main__":
    main()
