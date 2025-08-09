module list::list {
    use sui::object::{Self, UID, new};
    use sui::transfer;
    use std::string::{Self, String};
    use sui::tx_context::{Self, TxContext};

    public struct TodoItem has key {
        id: UID,
        description: String,
        Complete: bool,
    }

    public fun create_todo_item(description: String, ctx: &mut TxContext) {
        let todo = TodoItem {
            id: new(ctx),
            description,
            Complete: false,
        };
transfer::transfer(todo, tx_context::sender(ctx));
    }

    public fun mark_complete(todo: &mut TodoItem, _ctx: &mut TxContext) {
        todo.Complete = true;
    }
}
