import {BelongsToMany, Column, DataType, Model, Table} from "sequelize-typescript";
import {ApiProperty} from "@nestjs/swagger";
import {Artist} from "../artists/artists.model";
import {AlbumArtists} from "./album-artists.model";
import {UserFavouriteAlbums} from "../users/user-favourite-albums.model";
import {User} from "../users/users.model";

interface AlbumCreationAttrs{
    name:string;
    pictureURL:string;
}

@Table({tableName: 'albums'})
export class Album extends Model<Album, AlbumCreationAttrs> {
    @ApiProperty({example: 1})
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number

    @ApiProperty({example: 'Heavy Metal 2'})
    @Column({type: DataType.STRING(40), allowNull: false})
    name: string

    @ApiProperty({example: false})
    @Column({type: DataType.BOOLEAN, defaultValue: false})
    isPrivate: boolean

    @ApiProperty({example: 'ovbisut94ueslxzjvo.png'})
    @Column({type: DataType.STRING, defaultValue: ''})
    pictureURL: string

    @BelongsToMany(() => Artist, () => AlbumArtists)
    artists: Artist[]

    @BelongsToMany(() => User, () => UserFavouriteAlbums)
    favouriteOfUsers: User[]
}