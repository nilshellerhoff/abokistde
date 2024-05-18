<template>
  <div class="q-pa-md row justify-between">
    <div class="col-auto q-ma-lg order-xs-first">
      <q-avatar style="width: 80px; height: 80px">
        <q-img :src="props.channel?.thumbnail_url" />
      </q-avatar>
    </div>
    <div class="col-sm col-xs-12 self-center order-xs-last">
      <q-item-label overline class="text-subtitle-2"
        >{{ props.channel?.provider.name }}
      </q-item-label>
      <q-item-label class="text-h4">{{ props.channel?.name }}</q-item-label>
    </div>
    <div class="col-auto self-center q-pa-md-lg">
      <q-btn
        v-if="channel && !contentStore.getSubscriptionByChannel(channel)"
        label="Subscribe"
        color="primary"
        icon="add"
        style="width: 142px; margin: 2px 0"
        @click="subscribe"
      />
      <q-btn
        v-if="channel && contentStore.getSubscriptionByChannel(channel)"
        label="Manage"
        color="primary"
        icon="settings"
        style="width: 142px; margin: 2px 0"
        @click="openSubscriptionSettingsModal"
      />
      <br />
      <q-btn
        v-if="props.channel?.url"
        color="primary"
        label="channel"
        icon="open_in_new"
        :href="props.channel?.url"
        target="_blank"
        rel="noopener"
        style="width: 142px; margin: 2px 0"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { PublishingChannel } from 'src/types/api';
import { useContentStore } from 'stores/content-store';
import SubscriptionSettingsModal from 'components/Modals/SubscriptionSettingsModal.vue';
import { useQuasar } from 'quasar';

interface Props {
  channel?: PublishingChannel;
}

const props = defineProps<Props>();
const contentStore = useContentStore();
const $q = useQuasar();

const openSubscriptionSettingsModal = () => {
  const subscriptionId = props.channel
    ? contentStore.getSubscriptionByChannel(props.channel)?.id
    : undefined;
  if (subscriptionId) {
    $q.dialog({
      component: SubscriptionSettingsModal,
      componentProps: {
        subscriptionId,
      },
    });
  } else console.log('Subscription settings modal called without channel set!');
};

const subscribe = () => {
  if (props.channel) {
    contentStore.addSubscription({
      publishing_channel_id: props.channel.id,
      category_id: null,
    });
  }
};
</script>

<style>
@media (max-width: 600px) {
  .order-xs-last {
    order: 10000;
  }

  .order-xs-first {
    order: -10000;
  }
}

@media (min-width: 600px) {
  .order-xs-last {
  }

  .order-xs-first {
  }
}
</style>
