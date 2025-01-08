import {
    Controller,
    Get,
    Post,
    Body,
    Patch,
    Param,
    Delete,
    UseGuards,
    Req,
    UseInterceptors,
    UploadedFile
} from '@nestjs/common';
import { AlbumsService } from './albums.service';
import { AlbumDto } from './dto/album.dto';
import {ApiOperation, ApiResponse} from "@nestjs/swagger";
import {JwtAuthGuard} from "../auth/jwt-auth.guard";
import {JwtArtistsAuthGuard} from "../artists-auth/jwt-artists-auth.guard";
import {Album} from "./albums.model";
import {FileInterceptor} from "@nestjs/platform-express";
import {UpdateAlbumDto} from "./dto/update-album.dto";

@Controller('albums')
export class AlbumsController {
    constructor(private readonly albumService: AlbumsService) {}

    @ApiOperation({summary: 'Create a new album'})
    @ApiResponse({status: 200, type: Album})
    @UseGuards(JwtArtistsAuthGuard)
    @Post()
    create(@Req() req, @Body() albumDto: AlbumDto) {
        return this.albumService.create(albumDto, +req.artist.id);
    }

    @ApiOperation({summary: 'Get all album'})
    @ApiResponse({status: 200, type: [Album]})
    @Get('all')
    getAll() {
        return this.albumService.getAllAlbums();
    }

    @ApiOperation({summary: 'Get album with tracks'})
    @ApiResponse({status: 200, type: Album})
    @UseGuards(JwtAuthGuard)
    @Get('with-tracks/:albumId')
    getAlbumWithTracks(@Param('albumId') albumId: string) {
        return this.albumService.getAlbumWithTracksById(+albumId);
    }

    @ApiOperation({summary: 'Update album'})
    @ApiResponse({status: 200, type: Album})
    @UseGuards(JwtArtistsAuthGuard)
    @Patch(':albumId')
    @UseInterceptors(FileInterceptor('image'))
    update(@Req() req, @Body() dto: UpdateAlbumDto, @Param('albumId') albumId: string, @UploadedFile() image){
        return this.albumService.updateAlbum(+req.artist.id, +albumId, dto, image)
    }

    // @Delete(':id')
    // remove(@Param('id') id: string) {
    //     return this.albumService.remove(+id);
    // }
}
