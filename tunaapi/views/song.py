"""View module for handling requests about song types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist


class SongView(ViewSet):
    """Tuna Piano song types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song type
        
        Returns:
            Response -- JSON serialized song type
        """
        try:
            song = Song.objects.get(pk=pk)
            serializer = SingleSongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all song types

        Returns:
            Response -- JSON serialized list of song types
        """
        songs = Song.objects.all()
    
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized song instance
        """
        artist_id = Artist.objects.get(pk=request.data["artist_id"])

        song = Song.objects.create(
            title=request.data["title"],
            artist_id=artist_id,
            album=request.data["album"],
            length=request.data["length"],
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a song

        Returns:
            Response -- Empty body with 204 status code
        """

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        artist_id = Artist.objects.get(pk=request.data["artist_id"])
        song.artist_id = artist_id
        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            


class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song types
    """
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')
        depth = 1

class SingleSongSerializer(serializers.ModelSerializer):
  """JSON serializer for song types
    """
  class Meta:
      model = Song
      fields = ('id', 'title', 'artist_id', 'album', 'length', 'genres')
      depth = 2
