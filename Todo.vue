<template>
  <li class="d-flex align-items-center list-group-item">
    <input type="checkbox" name="" id="" @change="$emit('on-check')"
    v-bind:checked="completed" >
    <span
      class="btn border-0 flex-grow-1 text-left shadow-none text-break"
      :class="{ completed }"      
      v-if="!isEditing"
    >
      <span @dblclick="startEditing()">{{ task }}</span>
    </span>
    <form v-else class="flex-grow-1">
      <input
        type="text"
        class="form-control"
        v-model="newTodoTask"
        ref="newTodo" 
        @blur="finishEditing()"
        @keydown.enter="$event.target.blur()"
      />
    </form>
    <button
      @click="startEditing()"
      class="btn btn-outline-primary border-0 ml-2"
    >
      <span class="fa fa-edit"></span>
    </button>
    <button @click="$emit('on-delete')" class="btn btn-outline-danger border-0">
      <span class="fa fa-trash"></span>
    </button>
  </li>
</template>

<script>
export default {
  data() {
    return {
      isEditing: false,
      newTodoTask: ""
    };
  },
  props: {
    task: String,
    completed: Boolean
  },
  methods: {
    startEditing() {
      if (this.isEditing) {
        this.finishEditing();
      } else {
        this.newTodoTask = this.task;
        this.isEditing = true;
        this.$nextTick(() => this.$refs.newTodo.focus());
      }
    },
    finishEditing() {
      this.isEditing = false;
      if(this.newTodoTask != this.task)
        this.$emit("on-edit", this.newTodoTask);
    }
  }
};
</script>

<style lang="scss" scoped>
.completed {
  text-decoration: line-through;
}
</style>
