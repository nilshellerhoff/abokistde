<template>
  <q-layout view="hHh LpR lFf">
    <q-ajax-bar size="4px" />
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
        <div style="height: 50px" class="q-ma-sm" />

        <header-search />
        <header-menu />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <DrawerContent />
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import DrawerContent from 'components/DrawerContent.vue';
import HeaderMenu from 'components/HeaderBar/HeaderMenu.vue';
import HeaderSearch from 'components/HeaderBar/HeaderSearch.vue';

const leftDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>
