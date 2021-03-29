<template>
  <div class="container">
    <h1>{{ listName }}</h1>
    <div class="row mb-3">
      <create-todo @on-new-todo="addTodo($event)" />
    </div>
    <div class="row">
      <div class="col-12">
        <ul class="list-group">
          <todo
            v-for="(todo, index) in todos"
            :key="index"
            :task="todo.task"
            :completed="todo.status"
            @on-check="checkTodo(todo, $event)"
            @on-delete="deleteTodo(todo.id)"
            @on-edit="editTodo(todo, $event)"
          />
        </ul>
        <!-- <div v-html="pagination"></div> -->
      </div>
    </div>
  </div>
</template>

<script>
import Todo from "./Todo.vue";
import CreateTodo from "./CreateTodo.vue";
import axios from 'axios';
import Swal from 'sweetalert2'
const swalWithBootstrapButtons = Swal.mixin({
  customClass: {
    confirmButton: 'btn btn-success mx-2',
    cancelButton: 'btn btn-danger mx-2'
  },
  buttonsStyling: false
})


let isFetching= false;
let API_URL = 'https://localhost/api/todos'
const fetchingTodos = (_this, callback = null) => {
  if (!isFetching) {
    isFetching = true;
    axios.get(API_URL)
      .then(response => {
        //const pages = getPageRange(rs.data.pageInfo.current_page, rs.data.pageInfo.total);
        _this.todos = response.data.todos; _this.pagination = response.data.pagination
        isFetching = false;
        if (callback !== null) {
          callback.call();
        }
      })
      .catch(err => {
        // clearConsole();
        isFetching = false;
        console.log(err)
      })
  }
}
const handleActionDel = (_this, id) => {
  if (!isFetching) {
    axios.delete(API_URL+'/'+id)
    .then( (rs) => {
      console.log(rs)
      fetchingTodos(_this);
    } )
    .catch( err => {
      console.log(err)
    })
  }
}
const handleUpdate = (todo, newdata = null, callback = null) => {  
  console.log(newdata)
  axios.put(API_URL+'/'+todo.id, newdata)
  .then( (rs) => {
    console.log(rs)
    todo.status = rs.data.status
    todo.task = rs.data.task
    if (callback !== null) {
      callback.call();
    }
  } )
  .catch( err => {
    console.log(err)
    isFetching = false;
  })
}
export default {
  props: {
    listName: String,
  },
  data() {
    return {
      todos: null,
      pagination: null,
    }
  },
  mounted() {
    fetchingTodos(this)
  },
  methods: {    
    addTodo() {
      fetchingTodos(this)
    },
    checkTodo(todo) {
      handleUpdate(todo, {status: !todo.status})            
    },
    deleteTodo(id) {
      swalWithBootstrapButtons.fire({
        title: 'Are you sure to delete this todo ?',
        text: 'You won\'t be able to revert this!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          handleActionDel(this, id);
        }
      })      
      // this.todos = this.todos.filter(todo => todo !== deletedTodo);
    },
    editTodo(todo, newTodoTask) {
      handleUpdate(todo, {task:newTodoTask})      
    },
  },
  components: { Todo, CreateTodo },
};
</script>

<style scoped lang="scss"></style>
