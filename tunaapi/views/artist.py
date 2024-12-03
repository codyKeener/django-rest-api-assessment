"""View module for handling requests about artist types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist, Artist


class ArtistView(ViewSet):
    """Tuna Piano artist types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist type
        
        Returns:
            Response -- JSON serialized artist type
        """
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all artist types

        Returns:
            Response -- JSON serialized list of artist types
        """
        artists = Artist.objects.all()
    
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized artist instance
        """

        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a artist

        Returns:
            Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]

        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artist types
    """
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
        depth = 1
