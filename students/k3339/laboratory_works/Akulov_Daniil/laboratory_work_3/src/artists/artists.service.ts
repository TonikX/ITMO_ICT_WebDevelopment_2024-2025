import {HttpException, HttpStatus, Injectable} from '@nestjs/common';
import {InjectModel} from "@nestjs/sequelize";
import {CreateArtistDto} from "./dto/create-artist.dto";
import {Artist} from "./artists.model";
import {UpdateArtistDto} from "./dto/update-artist.dto";
import {FilesService} from "../files/files.service";
import {Album} from "../albums/albums.model";

@Injectable()
export class ArtistsService {
    constructor(@InjectModel(Artist) private artistRepository: typeof Artist,
                private filesService: FilesService) {}

    async createArtist(dto: CreateArtistDto) {
        const artist = await this.artistRepository.create(dto);
        return artist;
    }

    async updateArtist(artist, dto: UpdateArtistDto, image) {
        class Updates extends UpdateArtistDto{
            avatarURL?: string
        }
        const updates: Updates = {...dto}
        if(updates.username && artist.username !== updates.username) {
            const candidate = await this.getArtistByUsername(updates.username);
            if (candidate) {
                throw new HttpException("Artist with this username already exists", HttpStatus.BAD_REQUEST);
            }
        }
        if(image){
            updates.avatarURL = await this.filesService.createFile(image)
        }
        const [_, [updatedArtist]] = await this.artistRepository.update(updates, { where: { id: artist.id }, returning: true });
        return updatedArtist
    }

    async getAllArtists() {
        const artists = await this.artistRepository.findAll()
        return artists;
    }

    async getArtistById(id: number) {
        const artist = await this.artistRepository.findByPk(id);
        return artist
    }

    async getArtistByUsername(username: string) {
        const artist = await this.artistRepository.findOne({ where: {username} });
        return artist
    }

    async getAlbumsByArtistId(artistId: number) {
        const artist = await this.artistRepository.findByPk(artistId, {
            include: {
                model: Album,
                through: {
                    attributes: []
                }
            }
        })
        return artist.albums
    }
}
