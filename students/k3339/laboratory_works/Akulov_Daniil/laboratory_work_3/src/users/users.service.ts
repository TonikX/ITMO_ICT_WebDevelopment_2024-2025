import {HttpException, HttpStatus, Inject, Injectable, NotFoundException, Scope} from '@nestjs/common';
import {User} from "./users.model";
import {InjectModel} from "@nestjs/sequelize";
import {CreateUserDto} from "./dto/create-user.dto";
import {UpdateUserDto} from "./dto/update-user.dto";
import {FilesService} from "../files/files.service";
import {ArtistsService} from "../artists/artists.service";
import {Artist} from "../artists/artists.model";
import {UserBlockedArtists} from "./user-blocked-artists.model";
import {AlbumsService} from "../albums/albums.service";
import {UserFavouriteAlbums} from "./user-favourite-albums.model";
import {Album} from "../albums/albums.model";
import {AlbumArtists} from "../albums/album-artists.model";

@Injectable({ scope: Scope.REQUEST })
export class UsersService {
    constructor(@InjectModel(User) private userRepository: typeof User,
                @InjectModel(UserBlockedArtists) private userBlockedArtistsRepository: typeof UserBlockedArtists,
                @InjectModel(UserFavouriteAlbums) private userFavouriteAlbumsRepository: typeof UserFavouriteAlbums,
                private filesService: FilesService,
                private albumService: AlbumsService,
                private artistsService: ArtistsService) {}

    async createUser(dto: CreateUserDto) {
        const user = await this.userRepository.create(dto);
        return user;
    }

    async updateUser(user, dto: UpdateUserDto, image) {
        class Updates extends UpdateUserDto{
            avatarURL?: string
        }
        const updates: Updates = {...dto}
        if(updates.username && user.username !== updates.username) {
            const candidate = await this.getUserByUsername(updates.username);
            if (candidate) {
                throw new HttpException("User with this username already exists", HttpStatus.BAD_REQUEST);
            }
        }
        if(image){
            updates.avatarURL = await this.filesService.createFile(image)
        }
        const [_, [updatedUser]] = await this.userRepository.update(updates, { where: { id: user.id }, returning: true });
        return updatedUser
    }

    async getAllUsers() {
        const users = await this.userRepository.findAll()
        return users;
    }

    async getUserById(id: number) {
        const user = await this.userRepository.findByPk(id);
        return user
    }

    async getUserByUsername(username: string) {
        const user = await this.userRepository.findOne({ where: {username} });
        return user
    }

    async blockArtist(userId: number, artistId: number){
        const user = await this.userRepository.findByPk(userId);
        const artist = await this.artistsService.getArtistById(artistId);
        if (!artist || !user) {
            throw new HttpException('Artist not found', HttpStatus.NOT_FOUND);
        }
        await user.$add('blockedArtists', artistId)
        // await this.userBlockedArtistsRepository.create({userId: user.id, artistId});
        return
    }

    async unblockArtist(userId: number, artistId: number){
        const result = await this.userBlockedArtistsRepository.destroy({where: {userId, artistId}})
        if (result === 0) {
            throw new NotFoundException('Artist not found in blocked list');
        }
        return
    }

    async getBlockedArtistsByUserId(userId: number){
        // const user = await this.userRepository.findOne({where: {id}, include: [Artist]});
        // const res = await this.userBlockedArtistsRepository.findAll({where: {userId: id}});
        const user = await this.userRepository.findByPk(userId, {
            include: [{
                model: Artist,
                through: {
                    attributes: []
                },
                attributes: ['id', 'name', 'avatarURL']
            }]
        });
        return user.blockedArtists
    }

    async favouriteAlbum(userId: number, albumId: number){
        const user = await this.userRepository.findByPk(userId);
        const album = await this.albumService.getAlbumById(albumId);
        if (!album || !user || album.isPrivate) {
            throw new HttpException('Album not found', HttpStatus.NOT_FOUND);
        }
        await user.$add('favouriteAlbums', albumId)
        return
    }

    async unfavouriteAlbum(userId: number, albumId: number){
        const result = await this.userFavouriteAlbumsRepository.destroy({where: {userId, albumId}})
        if (result === 0) {
            throw new NotFoundException('Album not found in favourites list');
        }
        return
    }

    async getFavouriteAlbumsByUserId(userId: number){
        const user = await this.userRepository.findByPk(userId, {
            include: [{
                model: Album,
                through: {
                    model: AlbumArtists
                }
            }]
        });
        return user?.favouriteAlbums || []
    }
}
