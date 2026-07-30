
# =========================================================
# Robot Battle Game - GitHub Repository Version (main.py)
# Built with Python (Tkinter GUI - No External Libraries Required)
# Usage: python main.py
# =========================================================

import tkinter as tk
import random
import time
import threading

class RobotBattleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("ドラコニック インパクト vs ブラックライトニング")
        self.root.geometry("640x780")
        self.root.configure(bg="#0F172A")

        self.player_hp = 300
        self.max_player_hp = 300
        self.enemy_hp = 300
        self.max_enemy_hp = 300

        self.round_count = 1
        self.phase = "READY"
        self.tap_count = 0
        self.timer_seconds = 10.0
        self.total_taps = 0
        self.total_damage = 0

        self.roulette_numbers = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]

        self.build_ui()

    def build_ui(self):
        # Header Title Bar
        header = tk.Frame(self.root, bg="#1E293B", pady=10)
        header.pack(fill="x", padx=12, pady=10)

        self.title_label = tk.Label(
            header, text="⚡ ROBO BATTLE ARENA ⚡", 
            font=("Helvetica", 16, "bold"), fg="#38BDF8", bg="#1E293B"
        )
        self.title_label.pack(side="left", padx=10)

        self.round_label = tk.Label(
            header, text="ROUND 1", 
            font=("Helvetica", 12, "bold"), fg="#A855F7", bg="#1E293B"
        )
        self.round_label.pack(side="right", padx=10)

        # Arena Container
        arena = tk.Frame(self.root, bg="#0F172A")
        arena.pack(fill="both", expand=True, padx=12)

        # Enemy Card (Top)
        enemy_frame = tk.LabelFrame(
            arena, text=" 👾 ENEMY: ブラックライトニング 👾 ",
            font=("Helvetica", 12, "bold"), fg="#A855F7", bg="#1E293B", bd=2
        )
        enemy_frame.pack(fill="x", pady=8, ipady=10)

        self.enemy_hp_label = tk.Label(
            enemy_frame, text="HP: 300 / 300", 
            font=("Helvetica", 14, "bold"), fg="#F43F5E", bg="#1E293B"
        )
        self.enemy_hp_label.pack()

        # Player Card (Bottom)
        player_frame = tk.LabelFrame(
            arena, text=" 🤖 PLAYER: ドラコニック インパクト 🤖 ",
            font=("Helvetica", 12, "bold"), fg="#38BDF8", bg="#1E293B", bd=2
        )
        player_frame.pack(fill="x", pady=8, ipady=10)

        self.player_hp_label = tk.Label(
            player_frame, text="HP: 300 / 300", 
            font=("Helvetica", 14, "bold"), fg="#22C55E", bg="#1E293B"
        )
        self.player_hp_label.pack()

        # Interactive Controls
        ctrl_frame = tk.Frame(self.root, bg="#1E293B", pady=15)
        ctrl_frame.pack(fill="x", padx=12, pady=10)

        self.status_label = tk.Label(
            ctrl_frame, text="バトル開始ボタンを押してください！",
            font=("Helvetica", 12, "bold"), fg="#F8FAFC", bg="#1E293B"
        )
        self.status_label.pack(pady=4)

        self.action_btn = tk.Button(
            ctrl_frame, text="🚀 バトルスタート！", 
            font=("Helvetica", 14, "bold"), bg="#38BDF8", fg="#FFFFFF",
            activebackground="#0284C7", command=self.handle_action_click,
            width=22, height=2, bd=0
        )
        self.action_btn.pack(pady=8)

        # Logs Footer
        log_frame = tk.LabelFrame(self.root, text=" 📜 戦闘ログ 📜 ", fg="#94A3B8", bg="#0F172A")
        log_frame.pack(fill="x", padx=12, pady=8)

        self.log_text = tk.Text(log_frame, height=5, bg="#0F172A", fg="#CBD5E1", font=("Consolas", 10), bd=0)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.add_log("System", "ゲーム準備完了。対戦を開始してください。")

    def add_log(self, tag, msg):
        self.log_text.insert("1.0", f"[{tag}] {msg}\n")

    def handle_action_click(self):
        if self.phase == "READY" or self.phase == "GAME_OVER":
            self.start_player_turn()
        elif self.phase == "PLAYER_ATTACK":
            self.tap_count += 1
            self.total_taps += 1
            self.status_label.config(text=f"⏱️ 残り時間: {self.timer_seconds:.1f}s | 連打数: {self.tap_count}")
        elif self.phase == "PLAYER_RESULT":
            self.start_enemy_turn()
        elif self.phase == "ENEMY_RESULT":
            self.start_player_turn()

    def start_player_turn(self):
        if self.phase == "GAME_OVER":
            self.player_hp = 300
            self.enemy_hp = 300
            self.round_count = 1
            self.total_taps = 0
            self.total_damage = 0
            self.round_label.config(text=f"ROUND {self.round_count}")
            self.update_hp_display()

        self.phase = "PLAYER_ATTACK"
        self.tap_count = 0
        self.timer_seconds = 10.0
        self.action_btn.config(text="⚔️ 限界突破ラッシュ！ (連打！)", bg="#F43F5E")
        self.status_label.config(text="⏱️ 残り時間: 10.0s | 連打数: 0")

        def timer_thread():
            start_time = time.time()
            while True:
                elapsed = time.time() - start_time
                remaining = max(0.0, 10.0 - elapsed)
                self.timer_seconds = remaining
                self.root.after(0, lambda: self.status_label.config(
                    text=f"⏱️ 残り時間: {self.timer_seconds:.1f}s | 連打数: {self.tap_count}"
                ))
                if remaining <= 0:
                    break
                time.sleep(0.04)
            self.root.after(0, self.finish_player_turn)

        threading.Thread(target=timer_thread, daemon=True).start()

    def finish_player_turn(self):
        damage = self.tap_count * 2
        self.enemy_hp = max(0, self.enemy_hp - damage)
        self.total_damage += damage
        self.update_hp_display()

        self.add_log("Player", f"ROUND {self.round_count}: {self.tap_count}回連打！ {damage}ダメージ！")

        if self.enemy_hp <= 0:
            self.phase = "GAME_OVER"
            self.status_label.config(text="🎉 勝利！ 敵ロボを撃破しました！")
            self.action_btn.config(text="🔄 もう一度対戦する", bg="#22C55E")
        else:
            self.phase = "PLAYER_RESULT"
            self.status_label.config(text=f"連打結果: {self.tap_count}回 ({damage}ダメージ！)")
            self.action_btn.config(text="次へ (敵の攻撃ターン)", bg="#A855F7")

    def start_enemy_turn(self):
        self.phase = "ENEMY_ATTACK"
        self.action_btn.config(state="disabled", text="🎰 敵のルーレット回転中...", bg="#64748B")

        def roulette_thread():
            for i in range(22):
                val = random.choice(self.roulette_numbers)
                self.root.after(0, lambda v=val: self.status_label.config(
                    text=f"🎰 ブラックライトニング ルーレット中... [{v}]"
                ))
                time.sleep(0.06 + i * 0.01)

            chosen_damage = random.choice(self.roulette_numbers)
            self.root.after(0, lambda: self.finish_enemy_turn(chosen_damage))

        threading.Thread(target=roulette_thread, daemon=True).start()

    def finish_enemy_turn(self, damage):
        self.player_hp = max(0, self.player_hp - damage)
        self.update_hp_display()
        self.add_log("Enemy", f"ROUND {self.round_count}: ルーレット [{damage}]！ {damage}ダメージを受けた！")

        if self.player_hp <= 0:
            self.phase = "GAME_OVER"
            self.status_label.config(text="💥 敗北... プレイヤーロボ大破！")
            self.action_btn.config(state="normal", text="🔄 リトライする", bg="#F43F5E")
        else:
            self.phase = "ENEMY_RESULT"
            self.round_count += 1
            self.round_label.config(text=f"ROUND {self.round_count}")
            self.status_label.config(text=f"敵の攻撃: {damage}ダメージを受けた！")
            self.action_btn.config(state="normal", text="次へ (自分の攻撃ターン)", bg="#38BDF8")

    def update_hp_display(self):
        self.player_hp_label.config(text=f"HP: {self.player_hp} / {self.max_player_hp}")
        self.enemy_hp_label.config(text=f"HP: {self.enemy_hp} / {self.max_enemy_hp}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotBattleGame(root)
    root.mainloop()
