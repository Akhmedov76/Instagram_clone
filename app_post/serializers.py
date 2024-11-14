from rest_framework import serializers
class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Co
        fields = '__all__'