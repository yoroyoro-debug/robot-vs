# =========================================================
# Robot Battle Game - Streamlit Web Version (app.py)
# GUI依存なし (Tkinter不要) / Streamlit 専用Web実装
# 実行方法: streamlit run app.py
# =========================================================

import streamlit as st
import random

# --- 1. Pure State Logic (GUI非依存) ---
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
        self.battle_logs = []
        self.roulette_numbers = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]

    def add_log(self, tag, msg):
        self.battle_logs.insert(0, f"[{tag}] {msg}")

    def tap_attack(self):
        if self.phase == "PLAYER_ATTACK":
            self.tap_count += 1

    def finish_player_attack(self):
        self.last_player_damage = self.tap_count * 2
        self.enemy_hp = max(0, self.enemy_hp - self.last_player_damage)
        self.add_log("Player", f"ROUND {self.round_count}: {self.tap_count}連打！ {self.last_player_damage} ダメージを与えた！")
        
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

# --- 2. Streamlit Web Interface ---
def main():
    st.set_page_config(page_title="ロボットバトルアリーナ", page_icon="⚡", layout="centered")

    if "game" not in st.session_state:
        st.session_state.game = RobotBattleCore()

    game = st.session_state.game

    st.title("⚡ ROBO BATTLE ARENA")
    st.caption(f"ROUND {game.round_count} | ドラコニック インパクト vs ブラックライトニング")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🤖 ドラコニック")
        st.progress(game.player_hp / game.max_player_hp)
        st.write(f"**HP: {game.player_hp} / {game.max_player_hp}**")

    with col2:
        st.subheader("👾 ブラックライトニング")
        st.progress(game.enemy_hp / game.max_enemy_hp)
        st.write(f"**HP: {game.enemy_hp} / {game.max_enemy_hp}**")

    st.divider()

    # Dynamic Game Controls
    if game.phase == "READY":
        st.info("バトル準備完了！開始ボタンを押してください。")
        if st.button("🚀 バトルスタート！", use_container_width=True, type="primary"):
            game.phase = "PLAYER_ATTACK"
            st.rerun()

    elif game.phase == "PLAYER_ATTACK":
        st.warning("⚔️ 限界突破ラッシュ！ボタンを連打してください！")
        if st.button("🔥 アタック連打！ (+1)", use_container_width=True):
            game.tap_attack()

        st.metric("現在の連打数", f"{game.tap_count} 回", f"予想ダメージ: {game.tap_count * 2}")

        if st.button("⏱️ 攻撃確定 (ターン終了)", use_container_width=True, type="primary"):
            game.finish_player_attack()
            st.rerun()

    elif game.phase == "PLAYER_RESULT":
        st.success(f"攻撃完了！ {game.last_player_damage} ダメージを与えました！")
        if st.button("次へ (敵のターン)", use_container_width=True):
            game.execute_enemy_turn()
            st.rerun()

    elif game.phase == "ENEMY_RESULT":
        st.error(f"敵の攻撃！ {game.last_enemy_damage} ダメージを受けました！")
        if st.button("次へ (自分のターン)", use_container_width=True):
            game.phase = "PLAYER_ATTACK"
            game.tap_count = 0
            st.rerun()

    elif game.phase == "GAME_OVER":
        if game.player_hp > 0:
            st.balloons()
            st.success("🎉 WINNER! 敵ロボを撃破しました！")
        else:
            st.error("💥 GAME OVER... プレイヤーロボ大破")

        if st.button("🔄 もう一度対戦する", use_container_width=True, type="primary"):
            game.reset_game()
            st.rerun()

    st.divider()
    st.subheader("📜 戦闘ログ")
    for log in game.battle_logs[:8]:
        st.text(log)

if __name__ == "__main__":
    main()
