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

        <header-logo />
        <header-menu />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <DrawerContent />
    </q-drawer>

    <q-footer elevated class="lt-md">
      <q-tabs>
        <q-route-tab name="feed" icon="subscriptions" to="/feed" />
        <q-route-tab name="favorites" icon="favorite" to="/favorites" />
        <q-route-tab name="search" icon="search" to="/search" />
      </q-tabs>
    </q-footer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import DrawerContent from 'components/DrawerContent.vue';
import HeaderMenu from 'components/HeaderBar/HeaderMenu.vue';
import HeaderLogo from 'components/HeaderBar/HeaderLogo.vue';

const leftDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>
