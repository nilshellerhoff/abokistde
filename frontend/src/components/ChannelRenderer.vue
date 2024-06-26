<template>
  <q-item clickable :to="`/channel/${channel.id}`">
    <q-item-section avatar>
      <q-avatar>
        <q-img :src="channel.thumbnail_url" referrerpolicy="no-referrer">
          <template v-slot:error>
            <q-icon name="person" />
          </template>
        </q-img>
      </q-avatar>
    </q-item-section>
    <q-item-section>
      <q-item-label overline>
        {{ channel.provider.name }}
      </q-item-label>
      <q-item-label lines="1">
        {{ channel.name }}
      </q-item-label>
    </q-item-section>
    <q-item-section side>
      <q-btn
        v-if="showSubscriptionSettings"
        flat
        round
        dense
        icon="settings"
        @click.prevent="openSubscriptionSettingsModal"
      />
      <q-btn
        v-if="showAddSubscription"
        flat
        round
        dense
        icon="add"
        @click.prevent="subscribe"
      />
      <q-btn
        v-if="showChannelLink"
        flat
        round
        dense
        icon="info"
        :to="`/channel/${channel.id}`"
      />
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
import { PublishingChannel, UserSubscription } from 'src/types/api';
import { useQuasar } from 'quasar';
import SubscriptionSettingsModal from 'components/Modals/SubscriptionSettingsModal.vue';
import { useContentStore } from 'stores/content-store';

const contentStore = useContentStore();

interface Props {
  subscription?: UserSubscription;
  channel?: PublishingChannel;
  showSubscriptionSettings?: boolean;
  showAddSubscription?: boolean;
  showChannelLink?: boolean;
}

const props = defineProps<Props>();

const $q = useQuasar();

const openSubscriptionSettingsModal = () => {
  $q.dialog({
    component: SubscriptionSettingsModal,
    componentProps: {
      subscriptionId: props.subscription?.id,
    },
  });
};

const subscribe = () => {
  if (props.channel) {
    contentStore.addSubscription({
      publishing_channel_id: props.channel.id,
      category_id: null,
    });
  }
};

const channel = props.channel ?? props.subscription?.publishing_channel;
</script>
