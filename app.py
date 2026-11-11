<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stardew Trivia Boss Battles</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: #1a1a24;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow-y: auto;
            padding: 20px 0;
        }

        #game-container {
            position: relative;
            width: 800px;
            height: 500px;
            border: 4px solid #5d4037;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            background: #7ec850;
            overflow: hidden;
        }

        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }

        .hud {
            position: absolute;
            top: 10px;
            left: 10px;
            right: 10px;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
        }

        .bar-container {
            width: 220px;
            background: rgba(0, 0, 0, 0.6);
            padding: 8px 12px;
            border-radius: 6px;
            border: 2px solid #8d6e63;
        }

        .bar-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 4px;
            text-shadow: 1px 1px 2px #000;
        }

        .bar-outer {
            width: 100%;
            height: 16px;
            background: #333;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #000;
        }

        .bar-inner {
            height: 100%;
            width: 100%;
            transition: width 0.3s ease;
        }

        #player-hp { background-color: #4CAF50; }
        #boss-hp { background-color: #e53935; }

        #quiz-modal {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 650px;
            background: #fff8e7;
            border: 4px solid #5d4037;
            border-radius: 12px;
            padding: 16px 20px;
            color: #3e2723;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
            display: none;
            flex-direction: column;
            gap: 12px;
            z-index: 10;
        }

        .quiz-header {
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #8d6e63;
            margin: 0;
        }

        .quiz-question {
            font-size: 18px;
            font-weight: 700;
            margin: 0;
        }

        .quiz-options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }

        .btn-option {
            background: #d7ccc8;
            border: 2px solid #8d6e63;
            border-radius: 6px;
            padding: 10px;
            font-size: 15px;
            font-weight: 600;
            color: #3e2723;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .btn-option:hover {
            background: #bcaaa4;
            transform: translateY(-2px);
        }

        .overlay-screen {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.75);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 20;
        }

        .overlay-screen h1 {
            font-size: 36px;
            color: #ffeb3b;
            text-shadow: 2px 2px 4px #000;
            margin-bottom: 10px;
        }

        .overlay-screen p {
            font-size: 18px;
            margin-bottom: 20px;
        }

        .btn-main {
            background: #4caf50;
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 0 #2e7d32;
        }

        .btn-main:hover {
            background: #66bb6a;
        }

        .btn-main:active {
            transform: translateY(4px);
            box-shadow: none;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="500"></canvas>

        <div class="hud">
            <div class="bar-container">
                <div class="bar-title">Farmer Hero (Player)</div>
                <div class="bar-outer">
                    <div id="player-hp" class="bar-inner"></div>
                </div>
            </div>
            <div class="bar-container">
                <div class="bar-title" id="boss-name-display">Slime King</div>
                <div class="bar-outer">
                    <div id="boss-hp" class="bar-inner"></div>
                </div>
            </div>
        </div>

        <div id="quiz-modal">
            <p class="quiz-header" id="quiz-turn-indicator">Your Turn: Answer to Attack!</p>
            <p class="quiz-question" id="quiz-text">Question goes here?</p>
            <div class="quiz-options" id="quiz-options"></div>
        </div>

        <div id="overlay" class="overlay-screen">
            <h1 id="overlay-title">Stardew Trivia Boss Battles</h1>
            <p id="overlay-desc">Answer questions correctly to strike monsters and dodge incoming attacks!</p>
            <button id="btn-start" class="btn-main" onclick="startGame()">Start Game</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const questionsDB = [
            { q: "Which tool is used to till soil for planting?", options: ["Scythe", "Hoe", "Pickaxe", "Axe"], answer: 1 },
            { q: "How many days does a season last in Stardew Valley?", options: ["28 Days", "30 Days", "14 Days", "21 Days"], answer: 0 },
            { q: "What item restores energy and grows from seeds?", options: ["Wood", "Crops", "Stone", "Copper"], answer: 1 },
            { q: "Which tool is used to water dry crops?", options: ["Watering Can", "Bucket", "Hose", "Sprinkler"], answer: 0 },
            { q: "What building does Robin construct for animals?", options: ["Coop", "House", "Silo", "Greenhouse"], answer: 0 },
            { q: "Which season comes right after Spring?", options: ["Fall", "Winter", "Summer", "Spring 2"], answer: 2 },
            { q: "What tool breaks stones and rocks?", options: ["Hoe", "Pickaxe", "Fishing Rod", "Scythe"], answer: 1 },
            { q: "What entity sells seeds in town?", options: ["Willy", "Pierre", "Clint", "Robin"], answer: 1 }
        ];

        const bosses = [
            { name: "Forest Slime King", maxHp: 100, color: "#4CAF50", scale: 1 },
            { name: "Shadow Skeleton", maxHp: 150, color: "#9E9E9E", scale: 1.1 },
            { name: "Ancient Golem", maxHp: 200, color: "#795548", scale: 1.3 }
        ];

        let currentBossIndex = 0;
        let gameState = "MENU";
        let currentQuestion = null;

        const player = {
            x: 180, y: 320,
            hp: 100, maxHp: 100,
            targetX: 180,
            color: "#388E3C"
        };

        let boss = {
            x: 600, y: 300,
            hp: 100, maxHp: 100,
            targetX: 600,
            name: "Boss",
            color: "#e53935",
            scale: 1
        };

        let floatTexts = [];

        function addFloatingText(text, x, y, color) {
            floatTexts.push({ text, x, y, color, opacity: 1, life: 60 });
        }

        function startGame() {
            currentBossIndex = 0;
            player.hp = player.maxHp;
            loadBoss(currentBossIndex);
            document.getElementById('overlay').style.display = 'none';
            updateHUD();
            startPlayerTurn();
            gameLoop();
        }

        function loadBoss(index) {
            const b = bosses[index];
            boss.name = b.name;
            boss.maxHp = b.maxHp;
            boss.hp = b.maxHp;
            boss.color = b.color;
            boss.scale = b.scale;
            boss.x = 600;
            boss.targetX = 600;
            document.getElementById('boss-name-display').innerText = boss.name;
        }

        function updateHUD() {
            document.getElementById('player-hp').style.width = Math.max(0, (player.hp / player.maxHp) * 100) + '%';
            document.getElementById('boss-hp').style.width = Math.max(0, (boss.hp / boss.maxHp) * 100) + '%';
        }

        function getRandomQuestion() {
            const idx = Math.floor(Math.random() * questionsDB.length);
            return questionsDB[idx];
        }

        function showQuiz(isPlayerTurn) {
            currentQuestion = getRandomQuestion();
            const modal = document.getElementById('quiz-modal');
            const indicator = document.getElementById('quiz-turn-indicator');
            const qText = document.getElementById('quiz-text');
            const optionsDiv = document.getElementById('quiz-options');

            if (isPlayerTurn) {
                indicator.innerText = "YOUR TURN: Answer correctly to ATTACK!";
                indicator.style.color = "#2e7d32";
            } else {
                indicator.innerText = "DEFEND! Answer correctly to DODGE!";
                indicator.style.color = "#c62828";
            }

            qText.innerText = currentQuestion.q;
            optionsDiv.innerHTML = "";

            currentQuestion.options.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.className = 'btn-option';
                btn.innerText = opt;
                btn.onclick = () => handleAnswer(idx, isPlayerTurn);
                optionsDiv.appendChild(btn);
            });

            modal.style.display = 'flex';
        }

        function hideQuiz() {
            document.getElementById('quiz-modal').style.display = 'none';
        }

        function startPlayerTurn() {
            gameState = "PLAYER_TURN";
            showQuiz(true);
        }

        function startBossTurn() {
            gameState = "BOSS_TURN";
            showQuiz(false);
        }

        function handleAnswer(selectedIndex, isPlayerTurn) {
            hideQuiz();
            const isCorrect = selectedIndex === currentQuestion.answer;
            gameState = "ANIMATING";

            if (isPlayerTurn) {
                if (isCorrect) {
                    player.targetX = boss.x - 60;
                    setTimeout(() => {
                        const dmg = 35;
                        boss.hp -= dmg;
                        addFloatingText("-" + dmg + " CRIT!", boss.x, boss.y - 40, "#ffeb3b");
                        updateHUD();
                        player.targetX = 180;
                        setTimeout(() => checkBattleState("PLAYER"), 600);
                    }, 400);
                } else {
                    boss.targetX = boss.x + 40;
                    addFloatingText("BOSS DODGED!", boss.x, boss.y - 40, "#9e9e9e");
                    setTimeout(() => {
                        boss.targetX = 600;
                        setTimeout(() => startBossTurn(), 500);
                    }, 400);
                }
            } else {
                if (isCorrect) {
                    player.targetX = player.x - 50;
                    boss.targetX = player.x + 50;
                    setTimeout(() => {
                        addFloatingText("DODGED!", player.x, player.y - 40, "#81c784");
                        boss.targetX = 600;
                        player.targetX = 180;
                        setTimeout(() => startPlayerTurn(), 600);
                    }, 400);
                } else {
                    boss.targetX = player.x + 50;
                    setTimeout(() => {
                        const dmg = 25;
                        player.hp -= dmg;
                        addFloatingText("-" + dmg + " HIT!", player.x, player.y - 40, "#e53935");
                        updateHUD();
                        boss.targetX = 600;
                        setTimeout(() => checkBattleState("BOSS"), 600);
                    }, 400);
                }
            }
        }

        function checkBattleState(lastAttacker) {
            if (boss.hp <= 0) {
                currentBossIndex++;
                if (currentBossIndex >= bosses.length) {
                    showEndScreen(true);
                } else {
                    loadBoss(currentBossIndex);
                    updateHUD();
                    addFloatingText("NEW BOSS ARRIVED!", 400, 200, "#ffeb3b");
                    startPlayerTurn();
                }
            } else if (player.hp <= 0) {
                showEndScreen(false);
            } else {
                if (lastAttacker === "PLAYER") startBossTurn();
                else startPlayerTurn();
            }
        }

        function showEndScreen(won) {
            gameState = "GAMEOVER";
            const overlay = document.getElementById('overlay');
            const title = document.getElementById('overlay-title');
            const desc = document.getElementById('overlay-desc');
            const btn = document.getElementById('btn-start');

            overlay.style.display = 'flex';
            if (won) {
                title.innerText = "VICTORY!";
                desc.innerText = "You defeated all bosses with your agricultural wisdom!";
                btn.innerText = "Play Again";
            } else {
                title.innerText = "DEFEATED!";
                desc.innerText = "The monster overwhelmed you. Train your brain and try again!";
                btn.innerText = "Retry";
            }
        }

        function gameLoop() {
            player.x += (player.targetX - player.x) * 0.15;
            boss.x += (boss.targetX - boss.x) * 0.15;

            ctx.fillStyle = "#81c784";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#6d4c41";
            ctx.fillRect(50, 340, 700, 100);

            ctx.fillStyle = player.color;
            ctx.fillRect(player.x - 20, player.y - 40, 40, 50);
            ctx.fillStyle = "#ffcc80";
            ctx.fillRect(player.x - 15, player.y - 65, 30, 25);
            ctx.fillStyle = "#fbc02d";
            ctx.fillRect(player.x - 25, player.y - 70, 50, 10);

            ctx.fillStyle = boss.color;
            const bSize = 40 * boss.scale;
            ctx.beginPath();
            ctx.arc(boss.x, boss.y - bSize/2, bSize, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#fff";
            ctx.fillRect(boss.x - bSize/2, boss.y - bSize, 10, 10);
            ctx.fillRect(boss.x + bSize/4, boss.y - bSize, 10, 10);

            for (let i = floatTexts.length - 1; i >= 0; i--) {
                let ft = floatTexts[i];
                ctx.fillStyle = ft.color;
                ctx.font = "bold 20px 'Segoe UI'";
                ctx.fillText(ft.text, ft.x - 30, ft.y);
                ft.y -= 1;
                ft.life--;
                if (ft.life <= 0) floatTexts.splice(i, 1);
            }

            requestAnimationFrame(gameLoop);
        }
    </script>
</body>
</html>
