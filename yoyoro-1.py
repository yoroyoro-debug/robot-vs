package com.example.game

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

enum class BattlePhase {
    READY,
    PLAYER_ATTACK,
    PLAYER_RESULT,
    ENEMY_ATTACK,
    ENEMY_RESULT,
    GAME_OVER
}

enum class Winner {
    NONE,
    PLAYER,
    ENEMY
}

data class BattleLog(
    val id: Long = System.currentTimeMillis(),
    val message: String,
    val isPlayerAction: Boolean = true
)

data class BattleState(
    val playerHp: Int = 300,
    val maxPlayerHp: Int = 300,
    val enemyHp: Int = 300,
    val maxEnemyHp: Int = 300,
    val roundCount: Int = 1,
    val phase: BattlePhase = BattlePhase.READY,
    val tapCount: Int = 0,
    val timerSecondsLeft: Float = 10f,
    val lastPlayerDamage: Int = 0,
    val lastEnemyDamage: Int = 0,
    val currentRouletteIndex: Int = 0,
    val selectedRouletteValue: Int = 0,
    val isRouletteSpinning: Boolean = false,
    val winner: Winner = Winner.NONE,
    val totalPlayerTapsInMatch: Int = 0,
    val totalPlayerDamageDealt: Int = 0,
    val battleLogs: List<BattleLog> = emptyList()
)

class RobotBattleViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(BattleState())
    val uiState: StateFlow<BattleState> = _uiState.asStateFlow()

    val rouletteNumbers = listOf(0, 20, 40, 60, 80, 100, 120, 140, 160, 180)

    private var timerJob: Job? = null
    private var rouletteJob: Job? = null

    fun startPlayerTurn() {
        if (_uiState.value.phase == BattlePhase.GAME_OVER) {
            restartGame()
            return
        }

        _uiState.update {
            it.copy(
                phase = BattlePhase.PLAYER_ATTACK,
                tapCount = 0,
                timerSecondsLeft = 10.0f
            )
        }

        addLog("ROUND ${uiState.value.roundCount}: ドラコニック インパクトの攻撃ターン！ 10秒連打スタート！", true)

        timerJob?.cancel()
        timerJob = viewModelScope.launch {
            val startTime = System.currentTimeMillis()
            val totalDurationMs = 10000L

            while (true) {
                val elapsed = System.currentTimeMillis() - startTime
                val remainingMs = (totalDurationMs - elapsed).coerceAtLeast(0L)
                val remainingSec = remainingMs / 1000f

                _uiState.update { it.copy(timerSecondsLeft = remainingSec) }

                if (remainingMs <= 0) {
                    break
                }
                delay(40)
            }

            finishPlayerTurn()
        }
    }

    fun onTapAttackButton() {
        if (_uiState.value.phase != BattlePhase.PLAYER_ATTACK) return

        _uiState.update {
            it.copy(
                tapCount = it.tapCount + 1,
                totalPlayerTapsInMatch = it.totalPlayerTapsInMatch + 1
            )
        }
    }

    private fun finishPlayerTurn() {
        val taps = _uiState.value.tapCount
        val damage = taps * 2

        val newEnemyHp = (_uiState.value.enemyHp - damage).coerceAtLeast(0)

        _uiState.update {
            it.copy(
                enemyHp = newEnemyHp,
                lastPlayerDamage = damage,
                totalPlayerDamageDealt = it.totalPlayerDamageDealt + damage
            )
        }

        addLog("【連打判定】${taps}回タップ！ ブラックライトニングに${damage}ダメージ！", true)

        if (newEnemyHp <= 0) {
            _uiState.update {
                it.copy(
                    phase = BattlePhase.GAME_OVER,
                    winner = Winner.PLAYER
                )
            }
            addLog("🎉 勝利！ 敵ロボ「ブラックライトニング」を完全撃破！", true)
        } else {
            _uiState.update {
                it.copy(phase = BattlePhase.PLAYER_RESULT)
            }
        }
    }

    fun startEnemyTurn() {
        _uiState.update {
            it.copy(
                phase = BattlePhase.ENEMY_ATTACK,
                isRouletteSpinning = true
            )
        }

        addLog("ブラックライトニングの攻撃ターン！ 高出力ルーレット回転中...", false)

        rouletteJob?.cancel()
        rouletteJob = viewModelScope.launch {
            val totalSteps = 24
            for (i in 0 until totalSteps) {
                val nextIndex = (0 until rouletteNumbers.size).random()
                _uiState.update {
                    it.copy(currentRouletteIndex = nextIndex)
                }
                val delayTime = (60 + (i * 12)).toLong()
                delay(delayTime)
            }

            val finalIndex = (0 until rouletteNumbers.size).random()
            val chosenDamage = rouletteNumbers[finalIndex]

            val newPlayerHp = (_uiState.value.playerHp - chosenDamage).coerceAtLeast(0)

            _uiState.update {
                it.copy(
                    currentRouletteIndex = finalIndex,
                    selectedRouletteValue = chosenDamage,
                    lastEnemyDamage = chosenDamage,
                    isRouletteSpinning = false,
                    playerHp = newPlayerHp
                )
            }

            addLog("【敵ルーレット】[${chosenDamage}] を検出！ ドラコニック インパクトに${chosenDamage}ダメージ！", false)

            if (newPlayerHp <= 0) {
                _uiState.update {
                    it.copy(
                        phase = BattlePhase.GAME_OVER,
                        winner = Winner.ENEMY
                    )
                }
                addLog("💥 敗北... プレイヤーロボ「ドラコニック インパクト」が大破しました。", false)
            } else {
                _uiState.update {
                    it.copy(
                        phase = BattlePhase.ENEMY_RESULT,
                        roundCount = it.roundCount + 1
                    )
                }
            }
        }
    }

    fun restartGame() {
        timerJob?.cancel()
        rouletteJob?.cancel()
        _uiState.value = BattleState()
        addLog("ゲームをリセットしました。対戦スタートボタンを押してください。", true)
    }

    private fun addLog(message: String, isPlayer: Boolean) {
        _uiState.update {
            val newLogs = listOf(BattleLog(message = message, isPlayerAction = isPlayer)) + it.battleLogs
            it.copy(battleLogs = newLogs.take(30))
        }
    }
}
