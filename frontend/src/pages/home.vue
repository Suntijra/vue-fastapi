<template>
    <v-container fluid class="todo-list">
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>
              <v-text-field
                v-model="newTask"
                label="Add a new task"
                @keyup.enter="addTask"
                clearable
              />
              <v-btn color="primary" @click="addTask">Add</v-btn>
            </v-card-title>
            <v-list>
              <v-list-item-group>
                <v-list-item
                  v-for="(task, index) in tasks"
                  :key="index"
                  @click="removeTask(index)"
                >
                  <v-list-item-content>
                    <v-list-item-title>{{ task }}</v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn icon @click.stop="removeTask(index)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    name: 'TodoList',
    setup() {
      const newTask = ref('');
      const tasks = ref<string[]>([]);
  
      const addTask = () => {
        if (newTask.value.trim()) {
          tasks.value.push(newTask.value.trim());
          newTask.value = '';
        }
      };
  
      const removeTask = (index: number) => {
        tasks.value.splice(index, 1);
      };
  
      return {
        newTask,
        tasks,
        addTask,
        removeTask,
      };
    },
  });
  </script>
  
  <style scoped>
  .todo-list {
    min-height: 100vh;
    background: #f5f5f5;
  }
  </style>
  