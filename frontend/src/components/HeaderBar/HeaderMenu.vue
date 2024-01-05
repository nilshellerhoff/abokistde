<template>
  <q-btn flat icon="more_vert">
    <q-menu>
      <q-list style="min-width: 100px" class="q-px-md">
        <q-item clickable v-close-popup @click="isLoginDialogShown += 1">
          <q-item-section thumbnail
            ><q-icon name="logout"></q-icon
          ></q-item-section>
          <q-item-section>Logout</q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </q-btn>
  <LoginView :isDialogShown="isLoginDialogShown" />
</template>

<script setup lang="ts">
import LoginView from 'components/LoginView.vue';
import { ref } from 'vue';

const isLoginDialogShown = ref(0);
</script>
