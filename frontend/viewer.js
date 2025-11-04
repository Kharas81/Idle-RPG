// viewer.js – Zeichnet die Map als Emoji-Grid im Browser

// Emoji-Mapping für Tiles und Entities
const TILE_EMOJIS = {
    "floor": "⬜",
    "wall": "🟫",
    "start": "🟩",
    "goal": "🚪"
};
const ENTITY_EMOJIS = {
    "player": "🧑",
    "opponent": "👾",
    "chest": "💰"
};


// Lädt Map und Entities vom Backend
async function fetchMapState() {
    const resp = await fetch("/state");
    if (!resp.ok) {
        document.getElementById("map").innerText = "Fehler beim Laden der Map.";
        return null;
    }
    return await resp.json();
}

function renderMap(map) {
    let grid = [];
    for (let y = 0; y < map.height; y++) {
        let row = [];
        for (let x = 0; x < map.width; x++) {
            // Tile-Emoji
            let tile = map.tiles.find(t => t.x === x && t.y === y);
            let emoji = TILE_EMOJIS[tile?.type] || "⬜";
            // Entity-Emoji (falls vorhanden)
            let entity = map.entities.find(e => e.x === x && e.y === y);
            if (entity) {
                emoji = ENTITY_EMOJIS[entity.type] || emoji;
            }
            row.push(emoji);
        }
        grid.push(row.join(" "));
    }
    document.getElementById("map").innerText = grid.join("\n");
}

document.addEventListener("DOMContentLoaded", async () => {
    const map = await fetchMapState();
    if (map) renderMap(map);
});
