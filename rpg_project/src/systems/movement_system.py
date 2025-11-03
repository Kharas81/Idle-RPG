from rpg_project.src.models.ecs import EntityManager, PositionComponent, MoveIntentComponent
from rpg_project.src.services.world_state import WorldState

class MovementSystem:
    def update(self, world_state: WorldState):
        entities = world_state.entity_manager.get_entities_with(PositionComponent, MoveIntentComponent)
        for entity_id, components in entities.items():
            position = components[PositionComponent]
            move_intent = components[MoveIntentComponent]

            # Check for collisions or invalid moves (placeholder logic)
            new_x = position.x + move_intent.dx
            new_y = position.y + move_intent.dy

            # Update position if valid
            position.x = new_x
            position.y = new_y

            # Remove MoveIntentComponent after processing
            world_state.entity_manager.add_component(entity_id, None)