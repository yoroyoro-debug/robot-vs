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
import kotlin.random.Random

enum class BattlePhase {
    READY,
    PLAYER_ATTACK,
    PLAYER_RESULT,
    ENEMY_ATTACK,
    ENEMY_RESULT,
    GAME_OVER
}

data class BattleLog(
    val round: Int,
    val message: String,
    val isPlayerAction: Boolean
)

data class RobotBattleUiState(
    val phase: BattlePhase = BattlePhase.READY,
    val playerHp: Int = 300,
    val maxPlayerHp: Int = 300,
    val enemyHp: Int = 300,
    val maxEnemyHp: Int = 300,
    val selectedTimeLimit: Int = 10, // 10 or 20 seconds
    val timerSecondsLeft: Float = 10.0f,
    val tapCount: Int = 0,
    val lastPlayerDamage: Int = 0,
    val currentRouletteIndex: Int = 0,
    val selectedRouletteValue: Int = 0,
    val isRouletteSpinning: Boolean = false,
    val lastEnemyDamage: Int = 0,
    val roundCount: Int = 1,
    val winner: String? = null, // "PLAYER" or "ENEMY"
    val battleLogs: List<BattleLog> = emptyList(),
    val totalPlayerTapsInMatch: Int = 0,
    val totalPlayerDamageDealt: Int = 0
)

class RobotBattleViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(RobotBattleUiState())
    val uiState: StateFlow<RobotBattleUiState> = _uiState.asStateFlow()

    val rouletteNumbers = listOf(0, 20, 40, 60, 80, 100, 120, 140, 160, 180)

    private var timerJob: Job? = null
    private var rouletteJob: Job? = null

    fun setTimeLimit(seconds: Int) {
        if (_uiState.value.phase == BattlePhase.READY) {
            _uiState.update { it.copy(selectedTimeLimit = seconds, timerSecondsLeft = seconds.toFloat()) }
        }
    }

    fun startBattle() {
        timerJob?.cancel()
        rouletteJob?.cancel()
        _uiState.update {
            RobotBattleUiState(
                phase = BattlePhase.READY,
                playerHp = 300,
                enemyHp = 300,
                selectedTimeLimit = it.selectedTimeLimit,
                timerSecondsLeft = it.selectedTimeLimit.toFloat()
            )
        }
    }

    fun startPlayerTurn() {
        if (_uiState.value.phase != BattlePhase.READY && _uiState.value.phase != BattlePhase.ENEMY_RESULT) return

        val limit = _uiState.value.selectedTimeLimit
        _uiState.update {
            it.copy(
                phase = BattlePhase.PLAYER_ATTACK,
                timerSecondsLeft = limit.toFloat(),
                tapCount = 0,
                lastPlayerDamage = 0
            )
        }

        timerJob?.cancel()
        timerJob = viewModelScope.launch {
            val startTime = System.currentTimeMillis()
            val totalMillis = limit * 1000L

            while (_uiState.value.phase == BattlePhase.PLAYER_ATTACK) {
                val elapsed = System.currentTimeMillis() - startTime
                val remaining = (totalMillis - elapsed).coerceAtLeast(0L)
                val secondsLeft = remaining / 1000.0f

                _uiState.update { it.copy(timerSecondsLeft = secondsLeft) }

                if (remaining <= 0L) {
                    _uiState.update { it.copy(timerSecondsLeft = 0f) }
                    break
                }
                delay(30)
            }

            if (_uiState.value.phase == BattlePhase.PLAYER_ATTACK) {
                finishPlayerTurn()
            }
        }
    }

    fun onTapAttackButton() {
        val state = _uiState.value
        if (state.phase == BattlePhase.PLAYER_ATTACK && state.timerSecondsLeft > 0f) {
            _uiState.update {
                it.copy(
                    tapCount = it.tapCount + 1,
                    totalPlayerTapsInMatch = it.totalPlayerTapsInMatch + 1
                )
            }
        }
    }

    private fun finishPlayerTurn() {
        val taps = _uiState.value.tapCount
        val limit = _uiState.value.selectedTimeLimit
        val damagePerTap = if (limit == 20) 1 else 2
        val damage = taps * damagePerTap
        val newEnemyHp = (_uiState.value.enemyHp - damage).coerceAtLeast(0)
        val round = _uiState.value.roundCount

        val log = BattleLog(
            round = round,
            message = "ROUND $round: ${limit}秒間で $taps 回連打！ 相手に $damage ダメージ！",
            isPlayerAction = true
        )

        val isEnemyDefeated = newEnemyHp <= 0

        _uiState.update { state ->
            state.copy(
                phase = if (isEnemyDefeated) BattlePhase.GAME_OVER else BattlePhase.PLAYER_RESULT,
                enemyHp = newEnemyHp,
                lastPlayerDamage = damage,
                winner = if (isEnemyDefeated) "PLAYER" else null,
                battleLogs = listOf(log) + state.battleLogs,
                totalPlayerDamageDealt = state.totalPlayerDamageDealt + damage
            )
        }
    }

    fun startEnemyTurn() {
        if (_uiState.value.phase != BattlePhase.PLAYER_RESULT) return

        _uiState.update {
            it.copy(
                phase = BattlePhase.ENEMY_ATTACK,
                isRouletteSpinning = true,
                selectedRouletteValue = -1,
                lastEnemyDamage = 0
            )
        }

        rouletteJob?.cancel()
        rouletteJob = viewModelScope.launch {
            val chosenNumber = rouletteNumbers[Random.nextInt(rouletteNumbers.size)]
            var delayMs = 50L
            val totalCycles = 25 + Random.nextInt(10)

            for (i in 0 until totalCycles) {
                _uiState.update { state ->
                    val nextIdx = (state.currentRouletteIndex + 1) % rouletteNumbers.size
                    state.copy(currentRouletteIndex = nextIdx)
                }
                delay(delayMs)
                if (i > totalCycles - 10) {
                    delayMs += 30L
                }
            }

            val chosenIndex = rouletteNumbers.indexOf(chosenNumber)
            _uiState.update { state ->
                state.copy(
                    currentRouletteIndex = chosenIndex,
                    selectedRouletteValue = chosenNumber,
                    isRouletteSpinning = false
                )
            }

            delay(600)
            finishEnemyTurn(chosenNumber)
        }
    }

    private fun finishEnemyTurn(damage: Int) {
        val newPlayerHp = (_uiState.value.playerHp - damage).coerceAtLeast(0)
        val round = _uiState.value.roundCount
        val log = BattleLog(
            round = round,
            message = "ROUND $round: 相手のルーレットが [$damage] に停止！ $damage ダメージを受けた！",
            isPlayerAction = false
        )

        val isPlayerDefeated = newPlayerHp <= 0

        _uiState.update { state ->
            state.copy(
                phase = if (isPlayerDefeated) BattlePhase.GAME_OVER else BattlePhase.ENEMY_RESULT,
                playerHp = newPlayerHp,
                lastEnemyDamage = damage,
                winner = if (isPlayerDefeated) "ENEMY" else state.winner,
                battleLogs = listOf(log) + state.battleLogs,
                roundCount = if (isPlayerDefeated) state.roundCount else state.roundCount + 1
            )
        }
    }

    fun restartGame() {
        startBattle()
    }
}
