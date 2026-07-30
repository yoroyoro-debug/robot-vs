# =========================================================
# Robot Battle Game - Streamlit Cyber Edition (app.py)
# 
# 使い方:
#   1. pip install streamlit
#   2. streamlit run app.py
# =========================================================

import streamlit as st
import random

# --- 1. Pure State Logic (GUI依存なしの状態管理) ---
class RobotBattleCore:
    def __init__(self):
        self.player_hp = 300
        self.max_player_hp = 300
        self.enemy_hp = 300
        self.max_enemy_hp = 300

        self.round_count = 1
        self.phase = "READY"  # READY, PLAYER_ATTACK, PLAYER_RESULT, ENEMY_RESULT, GAME_OVER
        self.tap_count = 0
        self.last_player_damage = 0
        self.last_enemy_damage = 0
        self.battle_logs = ["ゲーム準備完了。対戦を開始してください。"]
        self.roulette_numbers = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]

    def add_log(self, tag, msg):
        self.battle_logs.insert(0, f"[{tag}] {msg}")

    def tap_attack(self):
        if self.phase == "PLAYER_ATTACK":
            self.tap_count += 1

    def finish_player_attack(self):
        self.last_player_damage = self.tap_count * 2
        self.enemy_hp = max(0, self.enemy_hp - self.last_player_damage)
        self.add_log("Player", f"ROUND {self.round_count}: {self.tap_count}連打！ {self.last_player_damage} ダメージ！")
        
        if self.enemy_hp <= 0:
            self.phase = "GAME_OVER"
        else:
            self.phase = "PLAYER_RESULT"

    def execute_enemy_turn(self):
        self.last_enemy_damage = random.choice(self.roulette_numbers)
        self.player_hp = max(0, self.player_hp - self.last_enemy_damage)
        self.add_log("Enemy", f"ROUND {self.round_count}: 敵ルーレット [{self.last_enemy_damage}]！ {self.last_enemy_damage} 被ダメージ！")

        if self.player_hp <= 0:
            self.phase = "GAME_OVER"
        else:
            self.phase = "ENEMY_RESULT"
            self.round_count += 1

    def reset_game(self):
        self.__init__()

# --- 2. Streamlit Custom Styled UI ---
def main():
    st.set_page_config(page_title="ロボットバトルアリーナ", page_icon="⚡", layout="centered")

    # サイバーUIカスタムCSS
    st.markdown("""
    <style>
        .stApp { background-color: #0F172A !important; color: #F8FAFC; }
        .robo-card {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border-radius: 16px;
            padding: 16px;
            border: 2px solid #334155;
            margin-bottom: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
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
        }
    </style>
    """, unsafe_allow_html=True)

    if "game" not in st.session_state:
        st.session_state.game = RobotBattleCore()

    game = st.session_state.game

    # タイトルバー
    st.markdown(f"""
    <div class="title-bar">
        <span style="font-size: 20px; font-weight: bold; color: #38BDF8;">🤖 ROBO BATTLE ARENA</span>
        <span style="font-size: 16px; font-weight: bold; color: #A855F7;">ROUND {game.round_count}</span>
    </div>
    """, unsafe_allow_html=True)

    # 敵ロボカード
    col_e1, col_e2 = st.columns([3, 1])
    with col_e1:
        st.markdown(f"""
        <div class="robo-card enemy-card">
            <div style="font-size: 12px; color: #A855F7; font-weight: bold;">ライバルロボ</div>
            <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">ブラックライトニング</div>
            <div class="hp-text-enemy">HP {game.enemy_hp} / {game.max_enemy_hp}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(game.enemy_hp / game.max_enemy_hp)
    with col_e2:
        st.image("https://api.iconify.design/game-icons:robot-antennas.svg?color=%23a855f7", width=80)

    st.markdown("<div style='text-align: center; font-weight: bold; color: #64748B; margin: 8px 0;'>⚡ VS BATTLE ⚡</div>", unsafe_allow_html=True)

    # プレイヤーロボカード
    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        st.markdown(f"""
        <div class="robo-card player-card">
            <div style="font-size: 12px; color: #38BDF8; font-weight: bold;">マイロボ</div>
            <div style="font-size: 20px; font-weight: bold; color: #FFFFFF;">ドラコニック インパクト</div>
            <div class="hp-text-player">HP {game.player_hp} / {game.max_player_hp}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(game.player_hp / game.max_player_hp)
    with col_p2:
        st.image("https://api.iconify.design/game-icons:mech-golem.svg?color=%2338bdf8", width=80)

    st.divider()

    # ゲームフェーズコントロール
    if game.phase == "READY":
        st.info("⚔️ バトル準備完了！下のボタンを押してバトルを開始しよう！")
        if st.button("🚀 バトルスタート！", use_container_width=True, type="primary"):
            game.phase = "PLAYER_ATTACK"
            st.rerun()

    elif game.phase == "PLAYER_ATTACK":
        st.warning("🔥 10秒間連打アタック！ ボタンを押しまくれ！")
        if st.button("⚡ 限界突破アタック！ (+1)", use_container_width=True):
            game.tap_attack()

        st.metric("現在の連打数", f"{game.tap_count} 回", f"与ダメージ: {game.tap_count * 2}")

        if st.button("⏱️ 攻撃確定 (ターン終了)", use_container_width=True, type="primary"):
            game.finish_player_attack()
            st.rerun()

    elif game.phase == "PLAYER_RESULT":
        st.success(f"💥 攻撃完了！ {game.last_player_damage} ダメージを与えた！")
        if st.button("次へ (敵のターン)", use_container_width=True):
            game.execute_enemy_turn()
            st.rerun()

    elif game.phase == "ENEMY_RESULT":
        st.error(f"⚡ 敵のルーレット攻撃！ {game.last_enemy_damage} ダメージを受けた！")
        if st.button("次へ (自分のターン)", use_container_width=True):
            game.phase = "PLAYER_ATTACK"
            game.tap_count = 0
            st.rerun()

    elif game.phase == "GAME_OVER":
        if game.player_hp > 0:
            st.balloons()
            st.success("🎉 WINNER! 敵ロボ『ブラックライトニング』を撃破！")
        else:
            st.error("💥 GAME OVER... ドラコニック インパクト大破")

        if st.button("🔄 もう一度対戦する", use_container_width=True, type="primary"):
            game.reset_game()
            st.rerun()

    st.divider()
    st.caption("📜 戦闘ログ")
    for log in game.battle_logs[:6]:
        st.code(log, language="text")

if __name__ == "__main__":
    main()
