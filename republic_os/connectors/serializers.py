from rest_framework import serializers
from .models import Connector, ConnectorSync
from .utils import get_connector_action


class ConnectorSerializer(serializers.ModelSerializer):
    buttons = serializers.SerializerMethodField('get_buttons')
    oauths = serializers.SerializerMethodField('get_oauths')

    def get_buttons(self, obj):

        get_buttons = get_connector_action(obj.republic_id, 'get_buttons')

        print(f'get_buttons: {get_buttons}')

        if get_buttons:
            print(obj.republic_id)
            print(get_buttons())
            return get_buttons()

        return None

    def get_oauths(self, obj):

        return obj.oauths.all().values('id')

    class Meta:
        model = Connector
        fields = '__all__'


class ConnectorSyncSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConnectorSync
        fields = '__all__'